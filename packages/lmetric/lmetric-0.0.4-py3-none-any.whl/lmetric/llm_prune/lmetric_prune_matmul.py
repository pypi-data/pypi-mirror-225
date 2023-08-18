# %%
import torch

import bitsandbytes as bnb
from bitsandbytes import functional as F

from pymeten import triton_benchmark_sizes, MetricConfig, MetricUnit
from scipy.stats import norm

# %%

def get_coo(x, threshold=0):
    """
    Returns a COO sparse tensor representation of the input tensor x based on a given threshold.

    Args:
        x (torch.Tensor): Input tensor.
        threshold (float, optional): Threshold value. Defaults to 0.

    Returns:
        torch.COOSparseTensor: COO sparse tensor representation of x.
    """

    #if threshold ==0:
    #    threshold = torch.quantile(x[:128][:2048].float(), ratio)
    #print(f'{ratio} {threshold}')
    idx = x <= threshold
    nnz = (idx == 1).sum().item()
    #print(f'nonzero ratio: {nnz / idx.numel()}')
    rows, cols = torch.where(idx)
    values = x[idx]
    cooA = F.COOSparseTensor(
        x.shape[0], x.shape[1], nnz, rows.int(), cols.int(), values
    )
    return cooA

def get_pt_sparse(x, threshold=0, representation='COO'):
    """
    Returns a PyTorch sparse tensor representation of the input tensor x based on a given threshold and representation type.

    Args:
        x (torch.Tensor): Input tensor.
        threshold (float, optional): Threshold value. Defaults to 0.
        representation (str, optional): Sparse tensor representation type. Defaults to 'COO'. options: COO CSR CSC BSR BSC

    Returns:
        torch.Tensor: Sparse tensor representation of x.
    """

    #if threshold ==0:
    #    threshold = torch.quantile(x[:128][:2048].float(), ratio)

    newx= torch.where(x>threshold, torch.tensor(0), x)
    if representation == 'COO':
        newx= newx.to_sparse_coo()
    elif representation == 'BSC':
        newx= newx.to_sparse_bsc()
    elif representation == 'BSR':
        newx= newx.to_sparse_bsr()
    elif representation == 'CSC':
        newx= newx.to_sparse_csc()
    elif representation == 'CSR':
        newx= newx.to_sparse_csr()
    else:
        newx= newx.to_sparse()
        print(type(newx))

    #print(newx)

    return newx

# %%
def lmetric_prune_matmul_Lx3HxH(seqlen=128, hidden_sizes=[2048 * i for i in range(1, 3)], dtype=torch.float16, metric='MS',
                                kernels=['torch', 'bnb_sparse'],
                                representations=['COO'],
                                ratios=[0.5]):
    """
    Computes metrics for pruning and matrix multiplication operations.

    Args:
        seqlen (int, optional): Sequence length. Defaults to 128.
        hidden_sizes (list, optional): List of hidden layer sizes. Defaults to [2048, 4096].
        dtype (torch.dtype, optional): Data type of the tensors. Defaults to torch.float16.
        metric (str, optional): Metric type ('TFLOPS', 'TBPS', or 'MS'). Defaults to 'MS'.
        kernels (list, optional): List of kernel types ('torch', 'bnb_sparse', 'torch_sparse'). Defaults to ['torch', 'bnb_sparse'].
        representations (list, optional): List of sparse tensor representations ('COO', 'CSC', 'CSR', 'BSC', 'BSR'). Defaults to ['COO'].
        ratios (list, optional): List of pruning ratios. Defaults to [0.5].
    """
    
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
        
    for k in kernels:
        assert k in ['torch', 'bnb_sparse', 'torch_sparse']
    for p in representations:
        assert p in ['COO', 'CSC', 'CSR', 'BSC', 'BSR']
    for r in ratios:
        assert r > 0 and r < 1
    if 'bnb_sparse' in kernels:
        assert dtype == torch.float16, 'bnb sparse only support float16'
    if 'torch_sparse' in kernels:
        assert dtype == torch.float32, 'torch sparse only support float32'
    
    inputs = {
        'x': lambda size: torch.randn(seqlen, 3*size, device='cuda', dtype=dtype),
        'w': lambda size: torch.randn(3*size, size, device='cuda', dtype=dtype),
        'wt': lambda size: torch.randn(size, 3*size, device='cuda', dtype=dtype),
    }

    for k in kernels:
        if k == 'bnb_sparse':
            for r in ratios:
                inputs.update({f'{k}_COO_{r}':lambda size:
                    get_coo(torch.randn(3*size, size, device='cuda', dtype=dtype), threshold=norm.ppf(r))
                })
        elif k == 'torch_sparse':
            for r in ratios:
                for p in representations:
                    inputs.update({f'{k}_{p}_{r}':lambda size:
                        get_pt_sparse(torch.randn(3*size, size, device='cuda', dtype=dtype), threshold=norm.ppf(r), representation=p)
                    })
                
    if 'torch' in kernels:
        kernelfns = {
            #'bnb.matmul': lambda **kwargs: 
            #    bnb.matmul(kwargs['x'], kwargs['wt']),
            'torch': lambda **kwargs: 
                torch.matmul(kwargs['x'], kwargs['w']),
        }
    else:
        kernelfns = {}

    for k in kernels:
        if k == 'bnb_sparse':
            for r in ratios:
                kernelfns.update({
                    f'{k}_COO_{r}': lambda **kwargs: 
                        F.spmm_coo(kwargs[f'{k}_COO_{r}'], kwargs['wt']),
                    
                })
        elif k == 'torch_sparse':
            for r in ratios:
                for p in representations:
                    kernelfns.update({f'{k}_{p}_{r}':lambda **kwargs:
                        torch.sparse.mm(kwargs[f'{k}_{p}_{r}'], kwargs['wt'])
                    })

    triton_benchmark_sizes(inputs, kernelfns, sizes=hidden_sizes, metric_config=metric_config)

# %%
if __name__ == '__main__':
    lmetric_prune_matmul_Lx3HxH()

# %%