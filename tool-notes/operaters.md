# About Deep Learning Programs

## 环境配置

+ 服务器新建环境和删除环境
  + 新建环境  
    ```conda create -n XXX python=3.9```
  or ```conda create --name XXX python=3.9```
  + 激活环境```conda activate XXX```
  + 退出环境```conda deactivate```
  + 删除环境
    ```conda remove -n XXX --all```

+ ```.yml```： 环境配置文件
  + 通过yml文件将Conda环境复制（移植）到其他服务器上（Windows 与 Linux 下的环境无法相互移植）
    > 如果需要使用Pytorch 和 Tensorflow等调用CUDA的库的话，需要保证两台机器具有相同的配置。
    > 假设需要把服务器A上的timer环境移植到服务器B上
  + 原服务器激活换取
    ```conda activate XXX```
  + 创建环境 
    ```conda env create -f environment.yml```
  + 生成环境配置文件
    ```conda env export > environment.yml```

+ ```requirements.txt```： 依赖包配置文件
  + 生成依赖包配置文件, 和安装依赖包
    ```pip freeze > requirements.txt```

```bash
  # 导出 conda 当前安装的环境中安装的包到requirements.txt中
    pip freeze > requirements.txt
    # 根据依赖文件安装所需库
    pip install -r requirements.txt
    # 或者 根据依赖文件安装所需库(根据清华镜像)
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

+ 通过依赖库```pipreqs```
    ```pip install pipreqs```
  + 生成依赖库文件 requirements.txt 
    ```pipreqs```
  + 安装依赖库 
    ```pip install -r requirements.txt```

## Debug

+ 运行断点```breakpoint()```

