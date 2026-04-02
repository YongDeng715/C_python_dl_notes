# numpy, matplotlib tutorial

## table of content
- [numpy, matplotlib tutorial](#numpy-matplotlib-tutorial)
  - [table of content](#table-of-content)
  - [numpy basics](#numpy-basics)
    - [size / ndim / shape / dtype](#size--ndim--shape--dtype)
  - [numpy 广播机制](#numpy-广播机制)
    - [升降维度操作: squeeze / unsqueeze](#升降维度操作-squeeze--unsqueeze)
  - [numpy 张量形状改变](#numpy-张量形状改变)
    - [扁平化操作： revel / flatten / reshape](#扁平化操作-revel--flatten--reshape)
    - [维度变化操作: transpose / moveaxis](#维度变化操作-transpose--moveaxis)
    - [复制张量: repeat / tile](#复制张量-repeat--tile)
    - [拼接操作： concatenate / stack / vstack / hstack / dstack](#拼接操作-concatenate--stack--vstack--hstack--dstack)
      - [concatenate / stack](#concatenate--stack)
      - [vstack / hstack / dstack](#vstack--hstack--dstack)
      - [conclusion](#conclusion)
      - [question](#question)
  - [numpy save](#numpy-save)
    - [np.save / np.load](#npsave--npload)
    - [h5py.File](#h5pyfile)
  - [matplotlib tutorial](#matplotlib-tutorial)
    - [基础绘图](#基础绘图)

## numpy basics

### size / ndim / shape / dtype

## numpy 广播机制

### 升降维度操作: squeeze / unsqueeze

- `np.squeeze(a)` (降维/压缩)：其核心功能是扫描数组的 shape，将所有长度严格为 1 的单维/冗余维度彻底剔除。这在清理经过多重神经网络层后附带无用占位维度的张量时极度重要。
- `np.expand_dims(a, axis)` / `np.newaxis` (升维/扩充)：其等同于 PyTorch 中的 `unsqueeze` 操作。它会在开发者指定的 axis 索引处，强制插入一个长度为 1 的全新维度。在 NumPy 语法糖中，使用 arr[:, np.newaxis] 是最常见且高效的原位升维手段，其中 `np.newaxis` 实质上只是 None 的别名。

潜在问题， 静默的错误广播 (Silent Broadcasting)：当试图将形状为 (N, 1) 的列向量与形状为 (N,) 的一维数组相加时，根据右对齐广播法则，系统会隐式将其扩充为 (1, N) 然后计算，结果生成一个 (N, N) 的矩阵，而不是报错。为了避免这种灾难性的静默逻辑错误，推荐在运算前使用 `np.newaxis` 显式强制对齐目标维度。


## numpy 张量形状改变

### 扁平化操作： revel / flatten / reshape

- `flatten()`：实例级方法，极端安全但开销昂贵。它必然在内存中开辟一块新的独立连续空间，并将所有元素复制进去，返回的永远是一个深拷贝（Copy）。
- `ravel()`：模块级库函数兼实例方法，主打性能极速优化。只要原始数组在内存地址上保持连续（C-contiguous），它就会原封不动地返回原始内存块的一个一维视图（View）；仅在遭遇跨步非连续断层时，才被迫退化生成拷贝。
- `reshape(-1)`：行为机制和内存策略与 `ravel()` 几乎等价，允许利用底层指针重排元数据。



潜在问题, 意外的数据污染：由于 `ravel()` 和 `reshape(-1)` 优先返回视图，新手在扁平化图像矩阵后直接对其做归一化或像素裁剪，会发现尚未参与计算的原始多维图像也被永久破坏了。若需修改，必须坚决调用 `flatten()` 或显式执行 `.copy()`。


### 维度变化操作: transpose / moveaxis

- `transpose()` (转置/重排)：允许传入一个包含所有轴索引排列组合的完整元组进行深度大洗牌（类似于深度学习中的 `permute`）。如果不传参（即 arr.T），它会将所有维度的顺序彻底逆转（例如 (0, 1, 2) 变成 (2, 1, 0)）。
- `swapaxes(axis1, axis2)`：专门用于仅仅互换其中两个指定轴的相对位置，而数组中的其余所有高维度的顺序维持原貌。
- `moveaxis(source, destination)`：将一个或多个轴从源位置“拔出”并精确安插到目标目的地索引处，其余未牵涉的轴依据原有顺序进行顺延填补，提供极高维度的自由穿梭能力。

应用过程中的潜在问题，维度迷失陷阱：在面对高达四五阶（如视频帧序列）的数据结构时，连续多次调用 `swapaxes` 会彻底让开发人员丧失对轴向所代表的物理意义（是高还是宽？）的掌控。此时推荐使用语义更明确的 `moveaxis`。此外，对 1D 数组执行 `transpose` 毫无效果，不会将其变成列向量，必须使用 `np.newaxis`


### 复制张量: repeat / tile
repeat函数功能：对数组中的元素进行连续重复复制
a为数组，repeats为重复的次数，axis表示数组维度

tile函数功能：对整个数组进行复制拼接

```python
numpy.repeat(a, repeats, axis=None)
a.repeats(repeats, axis=None)
 
numpy.tile(a, reps)
```

显式复制导致的内存溢出 (OOM) 问题：开发者有时为了使小张量与大张量尺寸对齐以进行加法运算，会使用 `tile` 强行将小张量放大并在内存中产生一个巨大的副本。正确姿势是充分利用 NumPy 无内存开销的广播机制 (Broadcasting)

### 拼接操作： concatenate / stack / vstack / hstack / dstack
   
#### concatenate / stack

**np.stack** ：添加一个**新维度** 。它接受两个或多个形状相同的数组，并返回一个维度更高的结果。
**np.concatenate** ：扩展**现有维度** 。它接受两个或多个数组，并沿指定的现有轴将它们连接起来。结果数组的维度数保持不变。

规则： 当需要添加额外轴来表示分组（例如，添加批次维度）时，如果要合并形状相同的数组，请使用 `np.stack` 。当想要通过沿现有轴追加数据来增加现有数组的长度（或宽度/深度）时，请使用 `np.concatenate` 。

```python
# Same 1D arrays: a = [1, 2, 3], b = [4, 5, 6]

# Using concatenate (extends the 0-th axis)
result1 = np.concatenate((a, b), axis=0)
print("Concatenate Result:", result1) # Output: [1, 2, 3, 4, 5, 6]
print("Shape:", result1.shape)        # Output: (6,) - Still 1D, just longer
```

`np.stack` 是为深度学习模型创建统一数据批次（例如，图像、时间序列窗口）的首选函数。轴控制： `axis` 参数决定新尺寸的插入位置 ：`axis=0` 将其插入到前面（用于批量大小）； `axis=-1` 将其插入到后面。

> 考虑这样一种情况：你有三个 64x64 的灰度图像。每个图像都是一个形状为 (64, 64) 二维 NumPy 数组。
```python
# Assume these are 2D arrays (e.g., loaded images)
img1 = np.ones((64, 64), dtype=np.uint8) * 10
img2 = np.ones((64, 64), dtype=np.uint8) * 50
img3 = np.ones((64, 64), dtype=np.uint8) * 90

images = [img1, img2, img3]  # Each shape: (64, 64)

# Stack the list of images along axis 0 to create a batch
dataset = np.stack(images, axis=0)
cated = np.concatenate(images, axis=0)
print("Final Dataset Shape:", dataset.shape) # Output: (3, 64, 64)
print("Final cated Shape:", cated.shape)     # Output: (192, 64)
```


#### vstack / hstack / dstack

NumPy设计了 `np.vstack`（垂直/按行堆叠）、`np.hstack`（水平/按列拼接）以及 `np.dstack`（深度堆叠）, 本质上都是先对输入序列进行维度提升的安全检查（如使用`atleast_1d` 、`atleast_2d` 等方法），继而调用底层的 `concatenate` 引擎.

`np.vstack` 和 `np.hstack` 都是 `np.concatenate` 便捷封装，而不是 `np.stack` 。它们不会添加新的维度，这对于从 2D 输入生成 3D 输出而言是一个关键区别。

在二维或三维的高阶场景中，逻辑十分清晰：`vstack`等同于沿`axis=0`进行纵向串接，而`hstack`等同于沿`axis=1`进行横向扩展。

对于一维数组的序列，`np.hstack` 仍然将其视作一维的标量序列，沿唯一的第0轴进行首尾相接的水平拼接，依然返回一个更长的一维向量。但是，`np.vstack` 认为“垂直堆叠”的意义在于生成行，它会强行将每一个输入的一维向量视作一个独立的 (1, N) 行向量，随后在垂直方向上叠层，最终输出一个标准的二维矩阵。专业程序通常选择利用 `np.column_stack`，将一维向量显式转化为独立的列向量后再行并排合并，从而彻底消除歧义。

```python
import numpy as np
a = np.array((1,2,3))
b = np.array((4,5,6))
print(np.concatenate((a,b), axis=0)) # array([1, 2, 3, 4, 5, 6])
print(np.hstack((a,b))) # array([1, 2, 3, 4, 5, 6])

print(np.concatenate((a,b), axis=1)) # IndexError: axis 1 out of bounds [0, 1)
print(np.vstack((a,b))) # array([[1,2,3], [4,5,6]])
print(np.column_stack((a,b))) # array([[1, 4], [2, 5], [3, 6]])


a = np.array([[1],[2],[3]])
b = np.array([[4],[5],[6]])
print(np.concatenate((a,b), axis=0)) # array([[1], [2], [3], [4], [5], [6]])
print(np.vstack((a,b))) # array([[1], [2], [3], [4], [5], [6]])

print(np.hstack((a,b))) # array([[1, 4], [2, 5], [3, 6]])
print(np.concatenate((a,b), axis=1)) # array([[1, 4], [2, 5], [3, 6]])
```


#### conclusion


| 张量拼接函数 | 底层调用链与核心目的 | 张量阶数（维度数量）变化 | 一维向量处理的特殊逻辑与副作用 |
| --- | --- | --- | --- |
| np.concatenate | 沿现有目标轴追加延展数据 | 无变化（阶数不变） | 仅能沿第0轴首尾相接, 不会转化为矩阵 |
| np.stack | 横跨新生成维度整合同构张量 |提升一阶（升维）| 将多个 1D 堆叠为 2D 矩阵 |
| np.vstack | 行级叠加（垂直拼合）| 二维以上无变化 | 隐式将1D视为行向量 | 拼接后强制转换为2D |
| np.hstack | 列级扩展（水平拼合）| 二维以上无变化 | 视1D为平面标量     | 拼接后依然是更长的1D |
| np.column_stack | 强制定向列组合| 强制确保至少为二维| 将1D视为列向量 | 是整合向量与矩阵的最佳实践 |

#### question

1. 可以使用 `np.stack` 处理不同数据类型（dtypes）的数组吗？可以，NumPy 会尝试寻找兼容的、更高精度的数据类型（例如，将 int8 和 float32 组合起来会得到一个 float32 数组）。但是，为了提高性能和一致性，最佳实践是在堆叠之前对所有输入数组的 `dtype` 进行规范化。
2. 什么时候应该使用 `np.dstack` 或 `np.vstack` 而不是 `np.stack` ？`np.vstack` 和 `np.hstack` 是 `np.concatenate` 的快捷方式，而不是 np.stack 快捷方式。当您需要沿着第三轴（axis=2） 堆叠数组时，请使用 np.dstack （深度堆栈），这通常用于合并颜色通道或深度图。

## numpy save 

### np.save / np.load

- `np.save('file.npy', arr)`：将单个 NumPy 数组序列化为极其高效的 `.npy` 原生二进制格式，能实现光速读写并无损保留数据精度与多维形状信息，在耗时上远胜文本格式（如CSV）数十倍。
- `np.savez('file.npz', a=arr1, b=arr2)`：构建一个轻量级的压缩归档包（`.npz`），其内部以类字典的形式分别封装了多个独立的 `.npy` 数据文件 。如果附加强烈压缩需求可使用 `np.savez_compressed` 。
- `np.load()`：多态读取函数。若载入 `.npy`，直接返回目标张量；若载入 `.npz`，则返回一个 NpzFile 懒加载字典容器 。

潜在问题，容器提取遗忘：直接对 `np.load('xxx.npz')` 的返回对象进行数学运算会引发错误，因为它返回的并不是张量，而是一个 NpzFile。开发者必须利用切片键（如 container['arr_0'] 或传入时的自定义命名）显式提取内部对象 

### h5py.File

HDF5 架构 (h5py)：这是为应对超过单机物理内存 (RAM) 极限的超大规模数据群（如数百 GB 的多维气候模型或图像集）而生的终极企业级方案。

它支持块级局部读取 (Chunking) 与切片，这代表你在访问一个 50GB 的矩阵的极小局部时，系统仅需调动极少内存，且该系统自带类似 Unix 系统的目录树层级管理。


潜在问题：
- **文件闭锁与句柄泄露**：遗忘使用 Python 的 with 上下文管理器封装 `h5py.File`，如果程序中途异常奔溃，这会导致庞大的持久化文件严重损坏;
- **指针与真值的混淆**：读取出的 `f['dataset_name']` 返回的是一个 HDF5 dataset 虚拟指针，并非 numpy 数组，直接作为参数丢入不支持该对象的函数会失效，必须加上 `[:]` 进行实际内存求值（如 `data = f['dataset'][:]`）。


## matplotlib tutorial 

### 基础绘图


- `plt.plot()`：最经典的数据流水线折线引擎，常接收序列作为坐标系基础并自动用线段连结离散点。
- `plt.subplots(nrows, ncols)` vs `plt.subplot()`：前者是当今力推的面向对象式范式，一键返回外层绘图布景窗口（fig）与轴控制句柄网格（axes），赋予开发者对各个子块独立精细渲染的能力；而后者是古老的 MATLAB 式遗留，容易造成全局状态状态机混乱与意外重写。
- `ax.imshow(image_tensor)`：专门用于展现二维热力图或彩色三维结构像素帧的直观图像输出函数。

潜在问题：
- 维度崩塌报错 (ValueError: x and y must have same first dimension)：若在数据清洗管线中利用布尔索引仅清除了Y轴（纵坐标）的离群噪点，而忘记对X轴作同步清除，传递给 plot 的两个张量尺寸将不再严密对等，会瞬间触发此异常。开发者必须防御性地使用 `assert len(x) == len(y)`。
- imshow Y轴图形学反转效应：使用 imshow 绘制热力矩阵时，其默认使用 `origin='upper'` 属性，导致图像的最顶端实则是第0行起步，Y轴指向朝下延展。如果在其上混合描绘标准的代数几何散点，必须强行覆写设定 `origin='lower'`。
- 拥挤的标签踩踏：在布局多个图表后，未执行 `plt.tight_layout()` 便急切呈现，导致子图的刻度与比邻图表的标题发生惨烈的像素叠压覆盖。