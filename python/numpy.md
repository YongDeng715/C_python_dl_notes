# numpy, matplotlib tutorial

## table of content
- [numpy, matplotlib tutorial](#numpy-matplotlib-tutorial)
  - [table of content](#table-of-content)
  - [numpy basics](#numpy-basics)
    - [size/ndim/shape/dtype](#sizendimshapedtype)
  - [numpy广播机制](#numpy广播机制)
    - [升降维度操作:squeeze/newaxis](#升降维度操作squeezenewaxis)
  - [numpy张量形状改变](#numpy张量形状改变)
    - [扁平化操作:revel/flatten/reshape(-1)](#扁平化操作revelflattenreshape-1)
    - [维度变化操作: transpose/moveaxis](#维度变化操作-transposemoveaxis)
    - [复制张量: repeat/tile](#复制张量-repeattile)
    - [拼接操作： concatenate/stack/vstack/hstack/dstack](#拼接操作-concatenatestackvstackhstackdstack)
      - [concatenate/stack](#concatenatestack)
      - [vstack/hstack/dstack](#vstackhstackdstack)
      - [conclusion](#conclusion)
      - [question](#question)
  - [numpy 数据持久化](#numpy-数据持久化)
    - [np.save/np.load/np.savez](#npsavenploadnpsavez)
    - [一些注意的问题](#一些注意的问题)
    - [h5py.File处理超大规模数据](#h5pyfile处理超大规模数据)
    - [h5py需要注意的问题](#h5py需要注意的问题)
  - [matplotlib tutorial](#matplotlib-tutorial)
    - [基础绘图](#基础绘图)

## numpy basics

### size/ndim/shape/dtype

| 属性         | 说明           | 返回值类型         | 典型用途        |
| ---------- | ------------ | ------------- | ----------- |
| `ndim`     | 数组的维度数（轴的数量） | `int`         | 判断数组是几维张量   |
| `shape`    | 数组在每个维度上的大小  | `tuple`       | 查看/修改数组形状   |
| `size`     | 数组中元素的总个数    | `int`         | 计算数据规模、内存估算 |
| `dtype`    | 数组元素的数据类型    | `numpy.dtype` | 类型检查、精度控制   |
| `itemsize` | 每个元素占用的字节数   | `int`         | 内存优化分析      |
| `nbytes`   | 整个数组占用的总字节数  | `int`         | 内存占用评估      |

注意: dtype 转换的精度损失

```python
arr_float = np.array([1.9, 2.8, 3.7])
arr_int = arr_float.astype(np.int32)  # 直接截断小数，不是四舍五入
print(arr_int)  # 输出: [1 2 3] - 精度丢失！
```

## numpy广播机制
广播（Broadcasting）是 NumPy 进行数组运算时的核心机制，它允许不同形状的数组进行算术运算，而无需显式复制数据。
**广播的核心规则**
- 维度对齐：从最后一个维度（最右边）开始，向左逐个比较两个数组的维度
- 维度兼容：两个维度兼容的条件是：
  - 维度相等，或
  - 其中一个维度为 1
- 缺失维度处理：维度数较少的数组，其形状会在左侧填充 1 直到维度数相同

### 升降维度操作:squeeze/newaxis

- `np.squeeze(a)` (降维/压缩)：其核心功能是扫描数组的 shape，将所有长度严格为 1 的单维/冗余维度彻底剔除。这在清理经过多重神经网络层后附带无用占位维度的张量时极度重要。
- `np.expand_dims(a, axis)` / `np.newaxis` (升维/扩充)：其等同于 PyTorch 中的 `unsqueeze` 操作。它会在开发者指定的 axis 索引处，强制插入一个长度为 1 的全新维度。在 NumPy 语法糖中，使用 arr[:, np.newaxis] 是最常见且高效的原位升维手段，其中 `np.newaxis` 实质上只是 None 的别名。

潜在问题， 静默的错误广播 (Silent Broadcasting)：当试图将形状为 (N, 1) 的列向量与形状为 (N,) 的一维数组相加时，根据右对齐广播法则，系统会隐式将其扩充为 (1, N) 然后计算，结果生成一个 (N, N) 的矩阵，而不是报错。为了避免这种灾难性的静默逻辑错误，推荐在运算前使用 `np.newaxis` 显式强制对齐目标维度。

```python
import numpy as np

# ========== squeeze 降维 ==========
arr = np.array([[[1, 2, 3]]])  # shape: (1, 1, 3)
print(f"原始形状: {arr.shape}")  # (1, 1, 3)

# 删除所有长度为 1 的维度
squeezed = np.squeeze(arr)
print(f"squeeze 后: {squeezed.shape}")  # (3,)

# 只删除指定维度
arr_2d = np.array([[[1, 2, 3]], [[4, 5, 6]]])  # shape: (2, 1, 3)
squeezed_axis1 = np.squeeze(arr_2d, axis=1)
print(f"只 squeeze axis=1: {squeezed_axis1.shape}")  # (2, 3)

# ========== expand_dims / newaxis 升维 ==========
arr_1d = np.array([1, 2, 3])  # shape: (3,)

# 方法 1: expand_dims
arr_2d = np.expand_dims(arr_1d, axis=0)  # shape: (1, 3)
arr_col = np.expand_dims(arr_1d, axis=1)  # shape: (3, 1)

# 方法 2: newaxis (更简洁，推荐)
arr_2d_new = arr_1d[np.newaxis, :]     # shape: (1, 3) - 行向量
arr_col_new = arr_1d[:, np.newaxis]    # shape: (3, 1) - 列向量
arr_3d_new = arr_1d[np.newaxis, :, np.newaxis]  # shape: (1, 3, 1)

print(f"\nnewaxis 行向量形状: {arr_2d_new.shape}")
print(f"newaxis 列向量形状: {arr_col_new.shape}")

# ========== 实际应用：批处理维度 ==========
image = np.random.rand(28, 28)  # 单张灰度图像
batch_image = image[np.newaxis, ...]  # shape: (1, 28, 28)
print(f"\n添加批次维度后: {batch_image.shape}")

# 多张图像堆叠
images = [np.random.rand(28, 28) for _ in range(10)]
batch = np.stack(images, axis=0)  # shape: (10, 28, 28)
print(f"10 张图像批次形状: {batch.shape}")
```

## numpy张量形状改变

### 扁平化操作:revel/flatten/reshape(-1)

- `flatten()`：实例级方法，极端安全但开销昂贵。它必然在内存中开辟一块新的独立连续空间，并将所有元素复制进去，返回的永远是一个深拷贝（Copy）。
- `ravel()`：模块级库函数兼实例方法，主打性能极速优化。只要原始数组在内存地址上保持连续（C-contiguous），它就会原封不动地返回原始内存块的一个一维视图（View）；仅在遭遇跨步非连续断层时，才被迫退化生成拷贝。
- `reshape(-1)`：行为机制和内存策略与 `ravel()` 几乎等价，允许利用底层指针重排元数据。

| 函数            | 返回类型   | 内存策略              | 性能 | 使用建议         |
| ------------- | ------ | ----------------- | -- | ------------ |
| `flatten()`   | 总是返回副本 | 深拷贝，新内存           | 较慢 | 需要保护原数组时使用   |
| `ravel()`     | 优先返回视图 | 视图（连续时）/ 副本（非连续时） | 快  | 性能优先，确认只读时使用 |
| `reshape(-1)` | 优先返回视图 | 视图（可能）/ 副本        | 快  | 最常用，灵活性高     |

潜在问题, 意外的数据污染：由于 `ravel()` 和 `reshape(-1)` 优先返回视图，新手在扁平化图像矩阵后直接对其做归一化或像素裁剪，会发现尚未参与计算的原始多维图像也被永久破坏了。若需修改，必须坚决调用 `flatten()` 或显式执行 `.copy()`。

```python
import numpy as np

arr_2d = np.array([[1, 2, 3], [4, 5, 6]])
print(f"原始数组:\n{arr_2d}")
print(f"原始形状: {arr_2d.shape}")

# ========== flatten() - 总是返回副本 ==========
flat_copy = arr_2d.flatten()
flat_copy[0] = 999
print(f"\nflatten() 修改后原数组:\n{arr_2d}")  # 原数组不变
print(f"flatten() 结果: {flat_copy}")

# ========== ravel() - 优先返回视图 ==========
arr_contiguous = np.array([[1, 2, 3], [4, 5, 6]])  # C-连续
ravel_view = arr_contiguous.ravel()
ravel_view[0] = 888
print(f"\nravel() 修改后原数组:\n{arr_contiguous}")  # 原数组被修改！

# 非连续数组的 ravel()
arr_non_contiguous = np.array([[1, 2, 3], [4, 5, 6]]).T  # 转置后非连续
print(f"\n转置后是否 C-连续: {arr_non_contiguous.flags['C_CONTIGUOUS']}")
ravel_copy = arr_non_contiguous.ravel()
ravel_copy[0] = 777
print(f"非连续数组 ravel() 修改后原数组:\n{arr_non_contiguous}")  # 原数组不变

# ========== reshape(-1) ==========
reshaped = arr_2d.reshape(-1)
print(f"\nreshape(-1) 结果: {reshaped}")

# reshape 可以指定 order
reshaped_f = arr_2d.reshape(-1, order='F')  # 按列展平
print(f"reshape(-1, order='F'): {reshaped_f}")  # [1 4 2 5 3 6]
```
 
### 维度变化操作: transpose/moveaxis

- `transpose()` (转置/重排)：允许传入一个包含所有轴索引排列组合的完整元组进行深度大洗牌（类似于深度学习中的 `permute`）。如果不传参（即 arr.T），它会将所有维度的顺序彻底逆转（例如 (0, 1, 2) 变成 (2, 1, 0)）。
- `swapaxes(axis1, axis2)`：专门用于仅仅互换其中两个指定轴的相对位置，而数组中的其余所有高维度的顺序维持原貌。
- `moveaxis(source, destination)`：将一个或多个轴从源位置“拔出”并精确安插到目标目的地索引处，其余未牵涉的轴依据原有顺序进行顺延填补，提供极高维度的自由穿梭能力。

应用过程中的潜在问题，维度迷失陷阱：在面对高达四五阶（如视频帧序列）的数据结构时，连续多次调用 `swapaxes` 会彻底让开发人员丧失对轴向所代表的物理意义（是高还是宽？）的掌控。此时推荐使用语义更明确的 `moveaxis`。此外，对 1D 数组执行 `transpose` 毫无效果，不会将其变成列向量，必须使用 `np.newaxis`

| 函数                     | 功能       | 参数       | 适用场景     | 性能    |
| ------------------------ | -------- | -------- | -------- | ----- |
| `transpose(axes)`        | 完全重排所有轴  | 完整的轴顺序元组 | 需要完全重排维度 | 快（视图） |
| `swapaxes(axis1, axis2)` | 交换两个指定轴  | 两个轴索引    | 只需交换两个维度 | 快（视图） |
| `moveaxis(source, dest)` | 移动轴到指定位置 | 源位置和目标位置 | 精确控制轴位置  | 快（视图） |
| `.T`                     | 完全反转轴顺序  | 无参数      | 二维矩阵转置   | 快（视图） |

```python
import numpy as np

# 创建 3D 数组: (depth, height, width) = (2, 3, 4)
arr_3d = np.arange(24).reshape(2, 3, 4)
print(f"原始形状: {arr_3d.shape}")  # (2, 3, 4)

# ========== transpose - 完全重排 ==========
transposed = np.transpose(arr_3d, (2, 1, 0)) # (2, 3, 4) -> (4, 3, 2)
print(f"transpose(2,1,0) 后: {transposed.shape}")  # (4, 3, 2)

# 默认 transpose (完全反转) 等价于 arr_3d.T
default_transposed = np.transpose(arr_3d)  # (4, 3, 2)
print(f"默认 transpose (反转): {default_transposed.shape}")

# ========== swapaxes - 交换两个轴 ==========
swapped = np.swapaxes(arr_3d, 0, 2) # 交换 axis 0 和 axis 2
print(f"swapaxes(0,2) 后: {swapped.shape}")  # (4, 3, 2)

# 两次 swapaxes 实现 transpose 效果 
swapped_twice = arr_3d.swapaxes(0, 2).swapaxes(0, 1)
print(f"两次 swapaxes 后: {swapped_twice.shape}")  # (3, 4, 2)

# ========== moveaxis - 精确移动轴 ==========
moved = np.moveaxis(arr_3d, 0, 2) # axis 0 -> axis 2
print(f"moveaxis(0,2) 后: {moved.shape}")  # (2, 3, 4) -> (3, 4, 2)

# 多轴同时移动：略（不常用，不要多次使用 `swapaxes` 和 `moveaxis`

# ========== 实际应用：图像格式转换 ==========
# PyTorch 格式 (N, C, H, W) → Matplotlib 格式 (N, H, W, C)
pytorch_images = np.random.rand(10, 3, 28, 28)  # 10张3通道28x28图像
matplotlib_images = np.moveaxis(pytorch_images, 1, -1)  # 将 C 轴移到最后
print(f"\nPyTorch 格式: {pytorch_images.shape}")
print(f"Matplotlib 格式: {matplotlib_images.shape}")  # (10, 28, 28, 3)
```

### 复制张量: repeat/tile
repeat函数功能：对数组中的元素进行连续重复复制
a为数组，repeats为重复的次数，axis表示数组维度

tile函数功能：对整个数组进行复制拼接

| 函数                         | 复制粒度    | 复制模式     | 内存预分配 | 典型应用      |
| -------------------------- | ------- | -------- | ----- | --------- |
| `repeat(a, repeats, axis)` | **元素级** | 连续重复单个元素 | 动态分配  | 数据增强、权重复制 |
| `tile(a, reps)`            | **数组级** | 整体数组平铺   | 预分配   | 批量扩展、模式重复 |


```python
numpy.repeat(a, repeats, axis=None)
a.repeats(repeats, axis=None)
 
numpy.tile(a, reps)
```

显式复制导致的内存溢出 (OOM) 问题：开发者有时为了使小张量与大张量尺寸对齐以进行加法运算，会使用 `tile` 强行将小张量放大并在内存中产生一个巨大的副本。正确姿势是充分利用 NumPy 无内存开销的广播机制 (Broadcasting)

### 拼接操作： concatenate/stack/vstack/hstack/dstack
   
#### concatenate/stack

**np.stack**: 添加一个**新维度**。它接受两个或多个形状相同的数组，并返回一个维度更高的结果。
**np.concatenate**: 扩展**现有维度**。它接受两个或多个数组，并沿指定的现有轴将它们连接起来。结果数组的维度数保持不变。

规则: 当需要添加额外轴来表示分组（例如，添加批次维度）时，如果要合并形状相同的数组，请使用 `np.stack` 。当想要通过沿现有轴追加数据来增加现有数组的长度（或宽度/深度）时，请使用 `np.concatenate` 。

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


#### vstack/hstack/dstack

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
| np.concatenate | 沿现有目标轴扩展 | 无变化（阶数不变） | 仅能沿第0轴首尾相接, 不会转化为矩阵 |
| np.stack | 横跨新生成维度整合同构张量 |提升一阶（升维）| 将多个 1D 堆叠为 2D 矩阵 |
| np.vstack | 行级叠加（垂直拼合）| 等效`concatenate(axis=0)` | 隐式将1D视为行向量， 拼接后强制转换为2D |
| np.hstack | 列级扩展（水平拼合）| 等效`concatenate(axis=1)` | 视1D为平面标量， 拼接后依然是更长的1D |
| np.column_stack | 强制定向列组合| 等效`hstack`(2D+)至少2维| 将1D视为列向量 | 是整合向量与矩阵的最佳实践 |
| np.dstack	|深度/通道堆叠 |等效 `concatenate(axis=2)`|	+1（3D）	先升维到 2D	|  
#### question

1. 可以使用 `np.stack` 处理不同数据类型（dtypes）的数组吗？可以，NumPy 会尝试寻找兼容的、更高精度的数据类型（例如，将 int8 和 float32 组合起来会得到一个 float32 数组）。但是，为了提高性能和一致性，最佳实践是在堆叠之前对所有输入数组的 `dtype` 进行规范化。
2. 什么时候应该使用 `np.dstack` 或 `np.vstack` 而不是 `np.stack` ？`np.vstack` 和 `np.hstack` 是 `np.concatenate` 的快捷方式，而不是 np.stack 快捷方式。当您需要沿着第三轴（axis=2） 堆叠数组时，请使用 np.dstack （深度堆栈），这通常用于合并颜色通道或深度图。

## numpy 数据持久化

### np.save/np.load/np.savez

- `np.save('file.npy', arr)`：将单个 NumPy 数组序列化为极其高效的 `.npy` 原生二进制格式，能实现光速读写并无损保留数据精度与多维形状信息，在耗时上远胜文本格式（如CSV）数十倍。
- `np.savez('file.npz', a=arr1, b=arr2)`：构建一个轻量级的压缩归档包（`.npz`），其内部以类字典的形式分别封装了多个独立的 `.npy` 数据文件 。如果附加强烈压缩需求可使用 `np.savez_compressed` 。
- `np.load()`：多态读取函数。若载入 `.npy`，直接返回目标张量；若载入 `.npz`，则返回一个 NpzFile 懒加载字典容器 。

潜在问题，容器提取遗忘：直接对 `np.load('xxx.npz')` 的返回对象进行数学运算会引发错误，因为它返回的并不是张量，而是一个 NpzFile。开发者必须利用切片键（如 container['arr_0'] 或传入时的自定义命名）显式提取内部对象 

```python
import numpy as np
# ========== 单个数组保存 ==========
arr = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float32)

# 保存为 .npy 格式
np.save('single_array.npy', arr)

# 加载
loaded = np.load('single_array.npy')
print(f"加载的数组:\n{loaded}")
print(f"dtype 保留: {loaded.dtype}")  # float32
print(f"shape 保留: {loaded.shape}")  # (2, 3)

# ========== 多个数组保存 ==========
arr1 = np.array([1, 2, 3])
arr2 = np.array([[4, 5], [6, 7]])
arr3 = np.random.rand(100, 100)

# 无压缩保存
np.savez('multiple_arrays.npz', arr1=arr1, arr2=arr2, image=arr3)
# 压缩保存（推荐用于大数组）
np.savez_compressed('compressed_arrays.npz', arr1=arr1, arr2=arr2, image=arr3)

# 加载 .npz 文件
data = np.load('multiple_arrays.npz')
print(f"\n.npz 文件中的键: {list(data.keys())}")
print(f"arr1: {data['arr1']}")
print(f"arr2:\n{data['arr2']}")
print(f"image 形状: {data['image'].shape}")
data.close()  # 显式关闭文件

# 使用 with 语句（推荐）
with np.load('multiple_arrays.npz') as data:
    arr1_loaded = data['arr1']
    arr2_loaded = data['arr2']
    # 自动关闭

# ========== 文本格式（小规模数据）==========
arr = np.array([[1.5, 2.5, 3.5], [4.5, 5.5, 6.5]])
# 保存为文本
np.savetxt('data.txt', arr, delimiter=',', fmt='%.2f')
# 从文本加载
loaded_txt = np.loadtxt('data.txt', delimiter=',')
print(f"\n从文本加载:\n{loaded_txt}")
```

### 一些注意的问题
1. 容器提取遗忘(`.npz` 文件): 不能直接对 NpzFile 对象进行运算, 必须先提取数组
2. `np.savetxt` 只能保存 1D 或 2D 数组
3. 文件路径和扩展名问题: `np.save`会自动添加`.npy`扩展名(如果不存在), 但加载时必须指定正确路径(包含`.npy`扩展名)
```python
arr = np.array([1, 2, 3])
np.save('myarray', arr)  # 实际保存为 'myarray.npy'

# loaded = np.load('myarray')  # 错误：找不到文件
loaded = np.load('myarray.npy')  # 正确
```
4. 内存映射大文件：对于超大数组，使用内存映射加载（不全部读入内存），只访问部分数据
```python
large_arr = np.random.rand(10000, 10000) # 超大数组的内存映射
np.save('large.npy', large_arr)

# 内存映射加载（不全部读入内存）
mmapped = np.load('large.npy', mmap_mode='r')
print(mmapped.shape)  # (10000, 10000)

subset = mmapped[100:200, 100:200]  # 只加载这部分到内存
```

### h5py.File处理超大规模数据

HDF5 架构 (h5py)：这是为应对超过单机物理内存 (RAM) 极限的超大规模数据群（如数百 GB 的多维气候模型或图像集）而生的终极企业级方案。

它支持块级局部读取 (Chunking) 与切片，这代表你在访问一个 50GB 的矩阵的极小局部时，系统仅需调动极少内存，且该系统自带类似 Unix 系统的目录树层级管理。

```python
import numpy as np
import h5py

# ========== 创建 HDF5 文件 ==========
with h5py.File('large_data.h5', 'w') as f:
    # 创建数据集
    dset = f.create_dataset('my_dataset', data=np.random.rand(100, 100))
    
    # 创建带压缩的数据集
    dset_compressed = f.create_dataset(
        'compressed',
        shape=(1000, 1000),
        dtype='float32',
        compression='gzip',  # gzip 压缩
        compression_opts=4   # 压缩级别 0-9
    )
    dset_compressed[...] = np.random.rand(1000, 1000)
    
    # 分块存储（支持高效切片）
    dset_chunked = f.create_dataset(
        'chunked',
        shape=(10000, 10000),
        dtype='float32',
        chunks=(100, 100),  # 每个块 100x100
        compression='gzip'
    )
    # 分块写入数据
    for i in range(0, 10000, 100):
        for j in range(0, 10000, 100):
            dset_chunked[i:i+100, j:j+100] = np.random.rand(100, 100)
    
    # 创建组（类似文件系统目录）
    group = f.create_group('images')
    group.create_dataset('image_1', data=np.random.rand(256, 256, 3))
    group.create_dataset('image_2', data=np.random.rand(256, 256, 3))
    
    # 添加属性
    dset.attrs['description'] = 'This is a test dataset'
    dset.attrs['created'] = '2024-01-01'

# ========== 读取 HDF5 文件 ==========
with h5py.File('large_data.h5', 'r') as f:
    # 查看文件结构
    print("文件顶层键:", list(f.keys()))
    
    # 访问数据集
    dset = f['my_dataset']
    print(f"\n数据集形状: {dset.shape}")
    print(f"数据集类型: {dset.dtype}")
    
    # 读取全部数据
    data = dset[:]  # 必须使用 [:] 读取实际数据
    print(f"读取的数据形状: {data.shape}")
    
    # 高效切片（只读取需要的部分）
    subset = dset[10:20, 10:20]
    print(f"切片数据形状: {subset.shape}")
    
    # 访问组
    images_group = f['images']
    print(f"\nimages 组中的数据集: {list(images_group.keys())}")
    
    # 读取属性
    print(f"\n属性: {dict(dset.attrs)}")

# ========== 追加模式 ==========
with h5py.File('large_data.h5', 'a') as f:
    # 创建新数据集
    if 'new_data' not in f:
        f.create_dataset('new_data', data=np.ones((10, 10)))
    
    # 调整现有数据集大小（仅支持 axis=0）
    if 'resizable' in f:
        dset = f['resizable']
    else:
        dset = f.create_dataset(
            'resizable',
            shape=(0, 10),
            maxshape=(None, 10),  # None 表示无限扩展
            dtype='float32'
        )
    
    # 追加数据
    current_size = dset.shape[0]
    new_data = np.random.rand(5, 10)
    dset.resize(current_size + 5, axis=0)
    dset[current_size:] = new_data
    print(f"\n调整后形状: {dset.shape}")
```

### h5py需要注意的问题
1. **文件闭锁与句柄泄露**：遗忘使用 Python 的 with 上下文管理器封装 `h5py.File`，如果程序中途异常奔溃，这会导致庞大的持久化文件严重损坏;
```python
# 错误：不使用 with，异常时文件损坏
f = h5py.File('data.h5', 'w')
f.create_dataset('test', data=[1, 2, 3])
# 如果这里发生异常，文件可能损坏！
f.close()

# 正确：使用 with 上下文管理器
with h5py.File('data.h5', 'w') as f:
    f.create_dataset('test', data=[1, 2, 3])
    # 即使发生异常，文件也会正确关闭
```
2. **指针与真值的混淆**：读取出的 `f['dataset_name']` 返回的是一个 HDF5 dataset 虚拟指针，并非 numpy 数组，直接作为参数丢入不支持该对象的函数会失效，必须加上 `[:]` 进行实际内存求值（如 `data = f['dataset'][:]`）。
```python
with h5py.File('data.h5', 'r') as f:
    dset = f['test']  # 这是 Dataset 对象，不是 numpy 数组！

    # 错误：直接用于计算
    # mean = np.mean(dset)  # 可能工作，但不推荐
    
    # 正确：先读取数据(读取全部 或 部分切片)
    data = dset[:]      # 读取全部
    subset = dset[0:10] # 或读取切片
    
    mean = np.mean(data)
```
3. 分块大小选择(分块太小：元数据开销大, 分块太大：切片效率低, 推荐：根据访问模式选择分块大小)
```python
# 如果主要按行访问
with h5py.File('data.h5', 'w') as f:
    dset = f.create_dataset(
        'row_access',
        shape=(10000, 1000),
        chunks=(1, 1000)  # 每行一个块
    )

# 如果主要按列访问
with h5py.File('data.h5', 'w') as f:
    dset = f.create_dataset(
        'col_access',
        shape=(10000, 1000),
        chunks=(10000, 1)  # 每列一个块
    )
``` 

## matplotlib tutorial 

### 基础绘图

- `plt.plot()`：最经典的数据流水线折线引擎，常接收序列作为坐标系基础并自动用线段连结离散点。
- `plt.subplots(nrows, ncols)` vs `plt.subplot()`：前者是当今力推的面向对象式范式，一键返回外层绘图布景窗口（fig）与轴控制句柄网格（axes），赋予开发者对各个子块独立精细渲染的能力；而后者是古老的 MATLAB 式遗留，容易造成全局状态状态机混乱与意外重写。
- `ax.imshow(image_tensor)`：专门用于展现二维热力图或彩色三维结构像素帧的直观图像输出函数。

| 函数                       | 功能     | 适用场景   | 返回值            |
| -------------------------- | -------- | ---------- | ----------------------- |
| `plt.plot()`               | 绘制折线图    | 时间序列、函数曲线  | Line2D 对象列表      |
| `plt.scatter()`            | 绘制散点图    | 数据分布、相关性分析 | PathCollection 对象 |
| `plt.bar()` / `plt.barh()` | 柱状图/条形图 | 类别比较        | BarContainer 对象       |
| `plt.hist()`               | 直方图        | 数据分布频率    | (counts, bins, patches) |
| `plt.imshow()`             | 显示图像/热力图 | 图像、矩阵可视化 | AxesImage 对象         |
| `plt.subplots()`           | 创建多子图    | 复杂布局       | (Figure, Axes 或 Axes数组) |


潜在问题：
- 维度崩塌报错 (ValueError: x and y must have same first dimension)：若在数据清洗管线中利用布尔索引仅清除了Y轴（纵坐标）的离群噪点，而忘记对X轴作同步清除，传递给 plot 的两个张量尺寸将不再严密对等，会瞬间触发此异常。开发者必须防御性地使用 `assert len(x) == len(y)`。
- imshow Y轴图形学反转效应：使用 imshow 绘制热力矩阵时，其默认使用 `origin='upper'` 属性，导致图像的最顶端实则是第0行起步，Y轴指向朝下延展。如果在其上混合描绘标准的代数几何散点，必须强行覆写设定 `origin='lower'`。
- 拥挤的标签踩踏：在布局多个图表后，未执行 `plt.tight_layout()` 便急切呈现，导致子图的刻度与比邻图表的标题发生惨烈的像素叠压覆盖。