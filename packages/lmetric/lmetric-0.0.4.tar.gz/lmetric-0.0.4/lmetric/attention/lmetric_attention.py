# %%
import math
import torch
import torch.nn.functional as F

from pymeten import triton_benchmark_sizes, MetricConfig, MetricUnit

from einops import rearrange

from typing import List

try:
    from flash_attn import flash_attn_qkvpacked_func
except:
    flash_attn_qkvpacked_func=None
from triton.ops.flash_attention import attention as attention_triton
try:
    import xformers.ops as xops
except:
    xops=None


torch.manual_seed(0)


# %%
def attention_pytorch(qkv, dropout_p=0.0, causal=True):
    """
    Arguments:
        qkv: (batch_size, seqlen, 3, nheads, head_dim)
        dropout_p: float
    Output:
        output: (batch_size, seqlen, nheads, head_dim)
    """
    batch_size, seqlen, _, nheads, d = qkv.shape
    q, k, v = qkv.unbind(dim=2)
    q = rearrange(q, 'b t h d -> (b h) t d')
    k = rearrange(k, 'b s h d -> (b h) d s')
    softmax_scale = 1.0 / math.sqrt(d)
    # Preallocate attn_weights for `baddbmm`
    scores = torch.empty(batch_size * nheads, seqlen, seqlen, dtype=qkv.dtype, device=qkv.device)
    scores = rearrange(torch.baddbmm(scores, q, k, beta=0, alpha=softmax_scale),
                       '(b h) t s -> b h t s', h=nheads)
    if causal:
        # "triu_tril_cuda_template" not implemented for 'BFloat16'
        # So we have to construct the mask in float
        causal_mask = torch.triu(torch.full((seqlen, seqlen), -10000.0, device=scores.device), 1)
        # TD [2022-09-30]: Adding is faster than masked_fill_ (idk why, just better kernel I guess)
        scores = scores + causal_mask.to(dtype=scores.dtype)
    attention = torch.softmax(scores, dim=-1)
    attention_drop = F.dropout(attention, dropout_p)
    output = torch.einsum('bhts,bshd->bthd', attention_drop , v)
    return output.to(dtype=qkv.dtype)


def lmetric_attention(batch_size: int or List[int]=32,
                                seqlen: int or List[int]=128,
                                num_heads: int or List[int]=[32 * i for i in range(1, 6)],
                                head_dim: int or List[int]=64,
                                dtype=torch.float16, metric='TFLOPS',
                                kernels=['torch', 'triton_flash', 'flash2', 'xformers'],
                                direction='fwd'
                                ):
    """
    Performs a attention module benchmarking with different kernels.

    Args:
        batch_size (int|list[int]): Batch size of the input data. Default is 32.
        seqlen (int|list[int]): Sequence length of the input data. Default is 128.
        num_heads (list[int]): Number of heads. Default is [32, 64, 96, 128, 160].
        head_dim (list[int]): The head dimension. Default is 64. triton_flash only support 64, and flash2 only support <256.
        dtype: Data type of the tensors. Default is torch.float16.
        metric (str): Metric to measure performance. Available options are 'TFLOPS', 'TBPS', or 'MS'. Default is 'TFLOPS'.
        kernels (list[str]): List of kernel functions to use. Default is ['torch', 'triton_flash', 'flash2', 'xformers'].
        direction (str): Direction of computation. Available options are 'fwd' (forward), 'bwd' (backward), or 'fwd_bwd'. Default is 'fwd'.

    Returns:
        None
    """
    
    dtype_bytes = torch.finfo(dtype).bits // 8
    
    comp_bs, comp_seqlen, comp_numhead, comp_headdim = False, False, False, False
    
    if isinstance(batch_size, List):
        comp_bs = True
    if isinstance(seqlen, List):
        comp_seqlen = True
    if isinstance(num_heads, List):
        comp_numhead = True
    if isinstance(head_dim, List):
        comp_headdim = True
    assert sum([comp_bs, comp_seqlen, comp_numhead, comp_headdim]) == 1, \
        "Must make one and only one of the following as a list: batch_size, \
        seqlen, num_heads, head_dim"

    if 'triton_flash' in kernels:
        assert head_dim == 64 or \
            isinstance(head_dim, List) and len(head_dim) == 1 and head_dim[0] == 64, \
                "triton_flash only support head_dim==64"
    
    def getTFLOPS(size, ms):
        if comp_bs:
            return dtype_bytes * size * seqlen**2 * num_heads * head_dim /ms
        if comp_seqlen:
            return dtype_bytes * batch_size * size**2 * num_heads * head_dim /ms
        if comp_numhead:
            return dtype_bytes * batch_size * seqlen**2 * size * head_dim /ms
        if comp_headdim:
            return dtype_bytes * batch_size * seqlen**2 * num_heads * size /ms

    def getTBPS(size, ms, is_forward=True):
        if comp_bs:
            if is_forward:
                return (4*dtype_bytes * size * seqlen * num_heads * head_dim +
                    (2*dtype_bytes+1) * size * seqlen**2 * num_heads * head_dim /64) / ms
            else:
                return (max(
                    2*dtype_bytes * size * seqlen * num_heads * head_dim,
                    2 * size * seqlen**2 * num_heads * head_dim/64) +
                    dtype_bytes * size * seqlen**2 * num_heads * head_dim/64) / ms
        if comp_seqlen:
            if is_forward:
                return (4*dtype_bytes * batch_size * size * num_heads * head_dim +
                    (2*dtype_bytes+1) * batch_size * size**2 * num_heads * head_dim /64) / ms
            else:
                return (max(
                    2*dtype_bytes * batch_size * size * num_heads * head_dim,
                    2 * batch_size * size**2 * num_heads * head_dim/64) +
                    dtype_bytes * batch_size * size**2 * num_heads * head_dim/64) / ms
        if comp_numhead:
            if is_forward:
                return (4*dtype_bytes * batch_size * seqlen * size * head_dim +
                    (2*dtype_bytes+1) * batch_size * seqlen**2 * size * head_dim /64) / ms
            else:
                return (max(
                    2*dtype_bytes * batch_size * seqlen * size * head_dim,
                    2 * batch_size * seqlen**2 * size * head_dim/64) +
                    dtype_bytes * batch_size * seqlen**2 * size * head_dim/64) / ms
        if comp_headdim:
            if is_forward:
                return (4*dtype_bytes * batch_size * seqlen * num_heads * size +
                    (2*dtype_bytes+1) * batch_size * seqlen**2 * num_heads * size /64) / ms
            else:
                return (max(
                    2*dtype_bytes * batch_size * seqlen * num_heads * size,
                    2 * batch_size * seqlen**2 * num_heads * size/64) +
                    dtype_bytes * batch_size * seqlen**2 * num_heads * size/64) / ms

    if metric == 'TFLOPS':
        metric_config=MetricConfig(
            MetricUnit.TFLOPS,
            calc_measure_fn=lambda size, ms:
                2*getTFLOPS(size, ms) if direction=='fwd' else \
                5*getTFLOPS(size, ms) if direction=='bwd' else \
                7*getTFLOPS(size, ms))
    elif metric == 'TBPS':
        metric_config=MetricConfig(
            MetricUnit.TBPS, # QKVO 8bsh, QK sm mask 5bs^2a
            # TODO: don't assume head_dim is 64
            calc_measure_fn=lambda size, ms:
                getTBPS(size, ms, True) if direction=='bwd' else \
                getTBPS(size, ms, False) if direction=='fwd' else \
                getTBPS(size, ms, True) + getTBPS(size, ms, False)
        )
    else:
        metric_config=MetricConfig(
            MetricUnit.MS)
    
    def get_qkv(size, separate=False):
        if comp_bs:
            if separate:
                return torch.randn(size, num_heads, seqlen, head_dim, device='cuda', dtype=dtype)
            else:
                return torch.randn(size, seqlen, 3, num_heads, head_dim, device='cuda', dtype=dtype)
        if comp_seqlen:
            if separate:
                return torch.randn(batch_size, num_heads, size, head_dim, device='cuda', dtype=dtype)
            else:
                return torch.randn(batch_size, size, 3, num_heads, head_dim, device='cuda', dtype=dtype)
        if comp_numhead:
            if separate:
                return torch.randn(batch_size, size, seqlen, head_dim, device='cuda', dtype=dtype)
            else:
                return torch.randn(batch_size, seqlen, 3, size, head_dim, device='cuda', dtype=dtype)
        if comp_headdim:
            if separate:
                return torch.randn(batch_size, num_heads, seqlen, size, device='cuda', dtype=dtype)
            else:
                return torch.randn(batch_size, seqlen, 3, num_heads, size, device='cuda', dtype=dtype)
        

    inputs = {
        'qkv' : lambda size:
            get_qkv(size, False),
        'q': lambda size:
            get_qkv(size, True),
        'k': lambda size:
            get_qkv(size, True),
        'v': lambda size:
            get_qkv(size, True),
    }

    kernelfns = {
        'torch': lambda **kwargs:
            attention_pytorch(kwargs['qkv'], causal=False),
        'triton_flash': lambda **kwargs:
            attention_triton(kwargs['q'], kwargs['k'], kwargs['v'], 64**(-0.5)),
        'flash2': lambda **kwargs:
            flash_attn_qkvpacked_func(kwargs['qkv']),
        'xformers': lambda **kwargs:
            xops.memory_efficient_attention(kwargs['q'], kwargs['k'], kwargs['v'],
                                            attn_bias=None,
                                            op=(xops.fmha.cutlass.FwOp, xops.fmha.cutlass.BwOp))
    }

    if flash_attn_qkvpacked_func is None:
        kernels.remove('flash2')
    if xops is None:
        kernels.remove('xformers')

    kernelfns = {k: kernelfns[k] for k in kernels}


    triton_benchmark_sizes(inputs,
                           kernelfns,
                           sizes=batch_size if comp_bs else \
                                seqlen if comp_seqlen else \
                                num_heads if comp_numhead else \
                                head_dim,
                           metric_config=metric_config)

if __name__ == '__main__':
    lmetric_attention(direction='fwd_bwd')
    #lmetric_attention(batch_size=[32 * i for i in range (1, 31, 5)], num_heads=32, direction='fwd_bwd')
    #lmetric_attention(seqlen=[128 * i for i in range (1, 9, 2)], num_heads=32, direction='fwd_bwd')
    #lmetric_attention(head_dim=[64 * i for i in range (1, 5)], kernels=['torch', 'flash2', 'xformers'], num_heads=32, direction='fwd_bwd')
# %%
