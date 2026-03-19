# FAISS

[TOC]

## Introduction

Reference: [The Faiss library](https://arxiv.org/abs/2401.08281)

+ installing from conda-forge  
  
    ```bash
    # CPU version
    $ conda install -c conda-forge faiss-cpu
    # GPU version
    $ conda install -c conda-forge faiss-gpu
    ```

+ Python and C++ version

## Faiss usage  

```python
def get_validation_recalls(r_list, q_list, k_values, gt,  
                           print_results=True, faiss_gpu=False, 
                            dataset_name='dataset without name ?', testing=False):
        
        embed_size = r_list.shape[1]
        if faiss_gpu:
            res = faiss.StandardGpuResources()
            flat_config = faiss.GpuIndexFlatConfig()
            flat_config.useFloat16 = True
            flat_config.device = 0
            faiss_index = faiss.GpuIndexFlatL2(res, embed_size, flat_config)
        # build index
        else:
            faiss_index = faiss.IndexFlatL2(embed_size)
        
        # add references
        faiss_index.add(r_list)

        # search for queries in the index
        dists, preds = faiss_index.search(q_list, max(k_values))

        np.savetxt("./output/{}_preds.txt".format(dataset_name), preds, fmt='%6.0f')
        np.savetxt("./output/{}_dists.txt".format(dataset_name), dists, fmt='%6.0f')
        if testing:
            return dists, preds
           
        
        # start calculating recall_at_k
        correct_at_k = np.zeros(len(k_values))
        for q_idx, pred in enumerate(preds):
            for i, n in enumerate(k_values):
                # if in top N then also in top NN, where NN > N
                if np.any(np.in1d(pred[:n], gt[q_idx])):
                    correct_at_k[i:] += 1
                    break
        
        correct_at_k = correct_at_k / len(preds)
        d = {k:v for (k,v) in zip(k_values, correct_at_k)}

        if print_results:
            print() # print a new line
            table = PrettyTable()
            table.field_names = ['K']+[str(k) for k in k_values]
            table.add_row(['Recall@K']+ [f'{100*v:.2f}' for v in correct_at_k])
            print(table.get_string(title=f"Performances on {dataset_name}")) 
        return d
```

we can use pytorch to implement the same function, but 
the performance is  not as good as the original one.

```python
import torch
import numpy as np
import torch.nn.functional as F

# 计算查询与参考之间的欧氏距离
def euclidean_distance(query, references):
    return torch.cdist(query, references)

# 计算查询与参考之间的余弦相似度
def cosine_similarity(query, references):
    # 归一化查询和参考
    query_norm = F.normalize(query, p=2, dim=1)
    references_norm = F.normalize(references, p=2, dim=1)
    # 计算余弦相似度
    similarity = torch.mm(query_norm, references_norm.t())
    return similarity

def get_topk_recalls(r_list, q_list, k_values,  
                           print_results=True,
                            dataset_name='dataset without name ?', 
                            dist:str='cosine'):
    # r_list: (num_references, fea_dim), q_list: (num_queries=1, fea_dim)
    assert dist in ['cosine', 'euclid'], 'dist must be cosine or euclid'

    # build references
    references = r_list 
    queries = q_list

    # search for queries in the index
    if (dist == 'euclid'):
        distances = euclidean_distance(queries, references)
        pred_dists, preds = torch.topk(distances, max(k_values), largest=False)
    else:
        similarities = cosine_similarity(queries, references) 
        pred_dists, preds = torch.topk(similarities, max(k_values), largest=True)
    
    if print_results:
        np.savetxt("./output/{}_predictions.txt".format(dataset_name, dist), preds, fmt='%6.0f')
    return pred_dists, preds
```

## Try FAINSS out

```python  
import faiss                   # make faiss available
index = faiss.IndexFlatL2(d)   # build the index, d=size of vectors 
# here we assume xb contains a n-by-d numpy matrix of type float32
index.add(xb)                  # add vectors to the index

print(index.ntotal)

# To perform a serch, xq is a n2-by-d matrix with query vectors
k = 4                          # we want 4 similar vectors
Dists, Pred_inds = index.search(xq, k)     # actual search
print(Pred_inds)
```

`Pred_inds` is an integer matrix. The output is something like this:

```bash
[[  0 393 363  78]
 [  1 555 277 364]
 [  2 304 101  13]]
```

Matrix `Dists` is the matrix of squared distances. It has the same shape as `Pred_Inds` and indicates for each result vector at the query’s squared Euclidean distance.

## 向量相似性搜索库(ScaNN) 

_[Accelerating Large-Scale Inference with Anisotropic Vector Quantization](https://arxiv.org/abs/1908.10396)_
_[Github Resource](https://github.com/google-research/google-research/tree/master/scann)_
_[MIPS: Learned Quantization](https://github.com/erikbern/ann-benchmarks#evaluated)_

## References

+ [Faiss: A library for efficient similarity search and clustering of dense vectors](https://github.com/facebookresearch/faiss)
+ the full documentation about Faiss on wiki page, [tutorial](https://github.com/facebookresearch/faiss/wiki/Getting-started),  [FAQ](https://github.com/facebookresearch/faiss/wiki/FAQ)
+ [Faiss: A library for efficient similarity search](https://engineering.fb.com/2017/03/29/data-infrastructure/faiss-a-library-for-efficient-similarity-search/)
+ [揭开 ScaNN 的神秘面纱：高效的向量相似性搜索](https://mp.weixin.qq.com/s/O9_eWwpA-B5IjKUSXfkJTA)