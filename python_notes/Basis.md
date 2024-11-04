# Python Tutorial Basis

[toc] 

## math

python math 库的常用模块变量
`math.e; math.inf; math.nan; math.pi; math.tau`

math 库中的常用函数和函数的使用区别。

```python
import math

math.ceil(x)     # 对一个数进行上取整
math.floor(x)    # 对一个数进行下取整
math.round(x)    # 四舍五入取整 =round(x)  
math.trunc(x)   # 返回 x 截断整数的部分，即返回整数部分，删除小数部分
# trunc() 对于正的 x 相当于 floor() ，对于负的 x 相当于 ceil()

math.isfinite(x)  # 判断 x 是否有限，x 既不是 inf（无穷大）也不是 NaN，则返回 True ，否则返回 False 
math.isinf(x)  # 判断 x 是否是无穷大，x 是正或负无穷大，则返回 True ，否则返回 False
math.isnan(x)   # 判断数字是否为 NaN（非数字），如果 x 是 NaN返回 True ，否则返回 False 
math.dist(p, q)
# 返回 p 与 q 两点之间的欧几里得距离，以一个坐标序列（或可迭代对象）的形式给出。 两个点必须具有相同的维度

# 以下是 math 的一些函数运算函数
acos, acosh, asin, asinh, atan, sin, sinh, cos, cosh, tan, tanh, 
pow(x, y), log, log10, exp, sqrt

math.degrees(x) = torch.deg2rad(x) # 将角度 x 从弧度转换为度数

math.radians(x) = torch.rad2deg(x) # 将角度 x 从度数转换为弧度
```

对比 torch 中常用的数学函数

```python
import torch

torch.abs(x) # 计算输入张量的每个元素绝对值

```

## logging



## argparase  

argsparse是python的命令行解析的标准模块，内置于python，不需要安装。这个库可以让我们直接在命令行中就可以向程序中传入参数并让程序运行。

```python
import argparse

parser = argparse.ArgumentParser(description="This is a description of our program")
parser.add_argument('-n', '--name', type=str, required=True, help='The name to print')
parser.add_argument('-a', '--age', type=int, required=True, help='The age to print')
args = parser.parse_args()

print(args.name)
print(args.age)
```


## Python Class 

 `@classmethod` 必须将一个类对象的引用作为第一个参数，其中 `cls` 代表的是类本身，而不是类的实例。

而 `@staticmethod` 可以不带任何参数, 调用静态方法，无需创建类的实例.

```python
class Date(object):
    def __init__(self, day=0, month=0, year=0):
        self.day = day
        self.month = month
        self.year = year

    @classmethod
    def from_string(cls, date_as_string):
        day, month, year = map(int, date_as_string.split('-'))
        date1 = cls(day, month, year)
        return date1

    @staticmethod
    def is_date_valid(date_as_string):
        day, month, year = map(int, date_as_string.split('-'))
        return day <= 31 and month <= 12 and year <= 3999


date2 = Date.from_string('11-09-2012')
is_date = Date.is_date_valid('11-09-2012')
```
