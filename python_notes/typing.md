# typing 模块笔记


typing 模块常用组件

```python
from typing import List, Tuple, Dict, Set, Union, Optional, Any, Callable, Iterable, TypedDict
```


`Callable` 用于指定函数类型。可以指定参数类型和返回类型。


`Iterable` 用于指示一个对象可以被迭代。该对象有一个 __iter__() 方法，返回一个迭代器，迭代器本身有一个 __next__() 方法，用于逐个返回集合中的元素。

```python
from typing import Iterable, Iterator

class MyIterable:
    def __init__(self, data):
        self.data = data

    def __iter__(self) -> Iterator[int]:
        for item in self.data:
            yield item


class MyIterator:
    def __init__(self, data):
        self.data = data
        self.index = 0

    def __next__(self) -> int:
        if self.index < len(self.data):
            result = self.data[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration

# 创建 MyIterable 实例
my_iterable = MyIterable([1, 2, 3])


# 使用 Iterable 类型注解
def process(iterable: Iterable[int]):
    for item in iterable:
        print(item)

# 调用函数，传入可迭代对象
process(my_iterable)
```


## 关于字典笔记

使用 `defaultdict` 动态构建多重字典

```python
from collections import defaultdict

db_dict = defaultdict(dict)
```