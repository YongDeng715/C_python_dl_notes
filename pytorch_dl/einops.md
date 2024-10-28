# 张量操作库einops（支持PyTorch）

einops 是一个用于处理和操作张量（tensor）的 Python 库，特别是在深度学习和科学计算领域。它提供了一种直观、简洁的方式来进行复杂的张量操作，例如重新排列、重塑、缩减和合并。主要功能如下

- **重新排列** `rearrange`: 重新排列张量的维度，类似于 NumPy 的 `transpose` 或 PyTorch 的 `permute`;
- **缩减** `reduce`: 沿指定维度进行归约操作，如求和、求均值等;
- **重复**`repeat`: 沿指定维度重复张量数据.

安装einops库
```bash
pip install einops
```

## 使用案例

```python
from einops import rearrange, reduce, repeat
import numpy as np

images = np.random.randn(32, 64, 64, 3)  # 32张64x64的RGB图像

# 重新排列为 (batch, channels, height, width)
images_rearranged = rearrange(images, 'b h w c -> b c h w')
print(images_rearranged.shape)  # 输出: (32, 3, 64, 64)

# 对张量进行求和，沿第4个维度求和
reduced = reduce(images, 'b h w c -> b h w', 'sum')
print(reduced.shape)  # 输出: (32, 64, 64)

# 对张量进行重复，沿第1个维度重复3次
repeated = repeat(images, 'b h w c -> b h w c', c=3)
print(repeated.shape)  # 输出: (32, 64, 64, 3)

```

## einops高级用法  

## einops和Pytorch, tensorflow
