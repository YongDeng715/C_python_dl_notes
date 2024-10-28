# Pytorch Tutorial  

## Pytorch Basis

1. 拼接函数：torch.stack()和torch.cat()

    **torch.stack()**: 沿着一个新维度对输入张量序列进行连接, 序列中所有的张量都应该为相同形状。

    ```python
    outputs = torch.stack(inputs, dim=0) → Tensor
    ```

    inputs : 待连接的张量序列。python的序列数据只有list和tuple。
    dim : 新的维度， 必须在0到len(outputs)之间。

    **torch.cat()**: 沿着指定维度连接张量序列。
    torch.cat() 和python中的内置函数cat()， 在使用和目的上，是没有区别的，区别在于前者操作对象是tensor.

    ```python  
    outputs = torch.cat(inputs, dim=0) → Tensor
    ```

    inputs : 待连接的张量序列，可以是任意相同Tensor类型的python 序列。
    dim : 选择的扩维, 必须在0到len(inputs[0])之间，沿着此维连接张量序列

2. 分割函数 torch.chunk(), torch.split()

    **torch.chunk()**: 将张量分割成若干块，返回一个元组，元组中每个元素是一个张量，张量的形状由参数sizes指定。

    ```python  
    outputs = torch.chunk(input, chunks, dim=0) → List of Tensors
    ```

    torch.chunk(k) 是将tensor切割为k个tensor
    input : 待分割的张量
    chunks : 要分割成的块数，或者一个列表，表示每块的大小
    dim : 要分割的维度

    **torch.split()**: 将张量分割成若干块，返回一个元组，元组中每个元素是一个张量，张量的形状由参数sizes指定。

    ```python  
    outputs = torch.split(tensor, split_size_or_sections, dim=0) → List of Tensors
    ```

    tensor : 待分割的张量
    split_size_or_sections : 每一块的大小，或者一个列表，表示每块的大小
    dim : 要分割的维度

    注：chunk是指定分割数量，split是指定分割完的tensor的样式。
3. 张量操作函数 torch.clamp()

    ```python  
    torch.clamp(input, min, max, out=None) -> Tensor
    ```

    将输入input张量每个元素的夹紧到区间 [min, max]，并返回结果到一个新张量.  

## torchvision.transforms 图像处理



## tensorboard 
