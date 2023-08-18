# **L**arge **M**odel m**etric**

A tool used to benchmark different kernels, algorithms developed for large models like LLM (Large Language Models).

## Install

`pip install lmetric`

## Metrics

### Matmul

floating point matmul:

```python
from lmetric import lmetric_matmul_fp16
lmetric_matmul_fp16(seqlen=128, sizes=[128 * i for i in range(2, 33, 5)], metrics='FLOPS', kernels=['triton', 'torch'])
# or just
lmetric_matmul_fp16()
```

![lmetric_matmul_fp16](https://raw.githubusercontent.com/OpenASI/LMetric/main/results/lmetric_matmul_fp16.png)

```python
from lmetric import lmetric_quant_matmul_Lx3HxH
lmetric_quant_matmul_Lx3HxH(seqlen=128, hidden_sizes=[2048 * i for i in range(1, 8)], dtype=torch.float16, metric='TFLOPS',
                                kernels=['torch', 'gptq', 'bnb_infer'],
                                bits=4, groupsize=128)
# or just
lmetric_quant_matmul_Lx3HxH()
```

![lmetric_quant_matmul](https://raw.githubusercontent.com/OpenASI/LMetric/main/results/lmetric_quant_matmul.png)

```python
from lmetric import lmetric_prune_matmul_Lx3HxH
lmetric_prune_matmul_Lx3HxH(seqlen=128, hidden_sizes=[2048 * i for i in range(1, 3)], dtype=torch.float16, metric='MS',
                                kernels=['torch', 'bnb_sparse'],
                                representations=['COO'],
                                ratios=[0.5])
# or just
lmetric_prune_matmul_Lx3HxH()
```

![lmetric_prune_matmul](https://raw.githubusercontent.com/OpenASI/LMetric/main/results/lmetric_prune_matmul.png)

### Attention

NOTE: Although you can directly installing flash-attn and xformers using
`pip install lmetric[attention]`
it is highly recommended that you install flash-attn by building from the source.
you can try `pytest tests/attention/test_flash_attn.py` to check your installation.

```python
from lmetric import lmetric_attention
lmetric_attention(batch_size=[32 * i for i in range (1, 31, 5)], seqlen=128, num_heads=32, head_dim=64,
                    dtype=torch.float16, metric='TFLOPS',
                    kernels=['torch', 'triton_flash', 'flash2', 'xformers'], direction='fwd_bwd')
```

The result comparison with batch_size from 32 to 832:
![lmetric_attention_bs](https://raw.githubusercontent.com/OpenASI/LMetric/main/results/lmetric_attention_bs_32_832.png)


```python
from lmetric import lmetric_attention
lmetric_attention(batch_size=32, seqlen=[128 * i for i in range (1, 9, 2)], num_heads=32, head_dim=64,
                    dtype=torch.float16, metric='TFLOPS',
                    kernels=['torch', 'triton_flash', 'flash2', 'xformers'], direction='fwd_bwd')
```

The result comparison with seqlen from 128 to 896:
![lmetric_attention_seqlen](https://raw.githubusercontent.com/OpenASI/LMetric/main/results/lmetric_attention_seqlen_128_896.png)

```python
from lmetric import lmetric_attention
lmetric_attention(batch_size=32, seqlen=128, num_heads=[32 * i for i in range(1, 6)], head_dim=64,
                    dtype=torch.float16, metric='TFLOPS',
                    kernels=['torch', 'triton_flash', 'flash2', 'xformers'], direction='fwd_bwd')
```

The result comparison with num_heads from 32 to 192:
![lmetric_attention_numheads](https://raw.githubusercontent.com/OpenASI/LMetric/main/results/lmetric_attention_numheads_32_192.png)

```python
from lmetric import lmetric_attention
lmetric_attention(batch_size=32, seqlen=128, num_heads=32, head_dim=[64 * i for i in range (1, 5)],
                    dtype=torch.float16, metric='TFLOPS',
                    kernels=['torch', 'triton_flash', 'flash2', 'xformers'], direction='fwd_bwd')
```

The result comparison with head_dim from 64 to 256:
![lmetric_attention_headdim](https://raw.githubusercontent.com/OpenASI/LMetric/main/results/lmetric_attention_headdim_64_256.png)


### LlamaCpp

Linux (-DLLAMA_BLAS is for OpenBLAS)
```
CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install llama-cpp-python
```

MacOS (https://github.com/abetlen/llama-cpp-python/blob/main/docs/install/macos.md)
```
CMAKE_ARGS="-DLLAMA_METAL=on" FORCE_CMAKE=1 pip install llama-cpp-python
```

Windows
```
$env:CMAKE_ARGS = "-DLLAMA_OPENBLAS=on"
$env:FORCE_CMAKE = 1
pip install llama-cpp-python
```

#### Autotune

```
python -m lmetric.llamacpp.lmetric_llamacpp --model_path <model_path> --n_batch 16 32 --n_threads 8 16
```

Change only one dimension to get a plot
```
python -m lmetric.llamacpp.lmetric_llamacpp --model_path <model_path> --n_batch 4 32 128 512 --n_threads 8
```

More commands
```
python -m lmetric.llamacpp.lmetric_llamacpp -h
```