# %%
import math
import torch

from pymeten import triton_benchmark_sizes, MetricConfig, MetricUnit

from lmetric.llm_quant.gptq_quant_linear import matmul248

import bitsandbytes as bnb
from bitsandbytes.nn import Int8Params
torch.manual_seed(0)


# %%

def get_bnb_weight_state(weight, threshold=6.0, has_fp16_weights=False, memory_efficient_backward=False):
    """
    Constructs a state and a bnb_weight dictionary.

    Args:
        weight (Tensor): The weight tensor.
        threshold (float, optional): Threshold value. Defaults to 6.0.
        has_fp16_weights (bool, optional): Flag indicating if the weights are in fp16 format. Defaults to False.
        memory_efficient_backward (bool, optional): Flag indicating if memory-efficient backward is enabled. Defaults to False.

    Returns:
        dict: A dictionary containing the 'bnb_weight' and 'state'.
    """

    bnb_weight = Int8Params(weight.T, has_fp16_weights=has_fp16_weights, requires_grad=has_fp16_weights).cuda(device='cuda')

    state = bnb.MatmulLtState()
    state.threshold = threshold
    state.has_fp16_weights = has_fp16_weights
    state.memory_efficient_backward = memory_efficient_backward
    state.is_training = has_fp16_weights
    if threshold > 0.0 and not has_fp16_weights:
        state.use_pool = True
    state.CB = bnb_weight.CB
    state.SCB = bnb_weight.SCB

    bnb_weight.CB = None
    bnb_weight.SCB = None

    return {'bnb_weight': bnb_weight, 'state': state}

def lmetric_quant_matmul_Lx3HxH(seqlen=128, hidden_sizes=[2048 * i for i in range(1, 8)], dtype=torch.float16, metric='TFLOPS',
                                kernels=['torch', 'gptq', 'bnb_infer'],
                                bits=4, groupsize=128):
    """
    Performs a quantized matrix multiplication benchmarking with different kernels.

    Args:
        seqlen (int, optional): Sequence length. Defaults to 128.
        hidden_sizes (list, optional): List of hidden sizes. Defaults to [2048 * i for i in range(1, 8)].
        dtype (torch.dtype, optional): Data type. Defaults to torch.float16.
        metric (str, optional): Metric for benchmarking. Defaults to 'TFLOPS'. options: TFLOPS, TBPS, MS
        kernels (list, optional): List of kernels to use. Defaults to ['torch', 'gptq', 'bnb_infer'].
        bits (int, optional): Number of bits for quantization. Defaults to 4.
        groupsize (int, optional): Group size for quantization. Defaults to 128.

    Returns:
        None
    """
    
    maxq = 2 ** bits - 1
    dtype_bytes = torch.finfo(dtype).bits // 8

    if metric == 'TFLOPS':
        metric_config=MetricConfig(
            MetricUnit.TFLOPS,
            calc_measure_fn=lambda size, ms: dtype_bytes*size*size*size / ms)
    elif metric == 'TBPS':
        metric_config=MetricConfig(
            MetricUnit.TBPS,
            calc_measure_fn=lambda size, ms: 3*dtype_bytes*size*size / ms)
    else:
        metric_config=MetricConfig(
            MetricUnit.MS)

    inputs = {
        'a' : lambda size:
            torch.randn((seqlen, 3*size), device='cuda', dtype=dtype),
        'weight': lambda size:
            torch.randn((3*size, size), device='cuda', dtype=dtype),
        'qweight': lambda size:
            torch.zeros((3*size // 32 * bits, size), device='cuda', dtype=torch.int32),
        'qzeros': lambda size:
            torch.zeros((math.ceil(3*size / groupsize), size // 32 * bits),
                        device='cuda', dtype=torch.int32),
        'scales': lambda size:
            torch.zeros((math.ceil(3*size / groupsize), size),
                        device='cuda', dtype=dtype),
        'g_idx': lambda size:
            torch.tensor([i // groupsize for i in range(3*size)],
                        device='cuda', dtype=torch.int32),
        'bnb_dict': lambda size: 
            get_bnb_weight_state(
                torch.randn((3*size, size), device='cuda', dtype=dtype),
            )

    }

    kernelfns = {
        'torch': lambda **kwargs:
            kwargs['a'] @ kwargs['weight'],
        'gptq': lambda **kwargs:
            matmul248(kwargs['a'], kwargs['qweight'], kwargs['scales'], kwargs['qzeros'], kwargs['g_idx'], bits, maxq),
        'bnb_infer': lambda **kwargs:
            bnb.matmul(kwargs['a'], kwargs['bnb_dict']['bnb_weight'], bias=None, state=kwargs['bnb_dict']['state'])
    }

    kernelfns = {k: kernelfns[k] for k in kernels}


    triton_benchmark_sizes(inputs, kernelfns, sizes=hidden_sizes, metric_config=metric_config)

if __name__ == '__main__':
    lmetric_quant_matmul_Lx3HxH()
# %%
