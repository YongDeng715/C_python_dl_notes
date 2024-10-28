# Windows, Linux安装 Anaconda并配置 Pytorch-GPU环境

[TOC]

## Windows 系统下安装 Anaconda

1. 官网下载 Anaconda 安装包， [Free Download|Anaconda](https://www.anaconda.com/download)  
    点击 FreeDownload, 提交邮箱， 点击 Download, 下载 Windows 系统的 Anaconda 安装包；
    自定义安装路径安装。
2. 清华源下载， [清华镜像源](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/)   
   下载适合Windows版本的Anaconda, 如 `windows-x86_64.exe`
   该方法下载速度更快


## Ubuntu 系统下安装 Anaconda


## Windows 系统下安装 CUDA 和 cuDNN(可选)

1. 查看电脑显卡驱动版本（这是显卡支持的最高CUDA版本）
   1. 方法一：cmd命令窗口输入 `nvidia-smi`， 查看显卡驱动版本为`CUDA Version: XX.X`;
   2. 方法二：点击NVIDIA控制面板 -> 系统信息 -> 组件，查看显卡驱动一栏信息为`NVIDIA CUDA 12.2.79 driver`
2. NVIDIA 官网下载 CUDA，链接：https://developer.nvidia.com/cuda-toolkit-archive
   其中 **安装CUDA Toolkit 版本 <= 电脑显卡驱动版本**, 安装在自定义文件夹
3. NVIDIA 官网下载 cuDNN，链接：https://developer.nvidia.com/cudnn
   - 选择与CUDA版本对应的cuDNN版本，下载cuDNN压缩包，解压到自定义文件夹
   - 查看是否安装成功，在cmd窗口或Anaconda Prompt 输入命令`nvcc -V`， 可以输出安装的CUDA版本信息
4. 下载 cuDNN（c需要注册，可以不装，这是个加速器）
   - 下载Windows版本的cuDNN，链接：https://developer.nvidia.com/rdp/cudnn-archive
   - 下载解压文件，有三个文件夹`bin`,`include`, `lib`,将这三个文件夹添加到CUDA文件夹中

## Windows 系统下配置 Pytorch-GPU环境

1. 首先自定义一个新环境并激活该环节
```shell
conda create -n pytorch python=3.10
conda activate pytorch
```
1. conda和pip配置清华源
   - Conda配置清华源
```shell
# 查看镜像源
conda config --remove-key channels

#添加镜像源
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/pro
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2

#终端显示包从哪个channel下载，以及下载地址是什么
conda config --set show_channel_urls yes
```
   - pip配置清华源
```shell
# 临时配置，[some-package] 代表你需要安装的包
pip install [some-package] -i https://pypi.tuna.tsinghua.edu.cn/simple

# 永久配置
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```
   - 国内常用镜像源

> 清华大学开源软件镜像站：https://pypi.tuna.tsinghua.edu.cn/simple
> 阿里云开源镜像站：https://mirrors.aliyun.com/pypi/simple/
> 豆瓣：https://pypi.douban.com/simple/
> 中国科技大学 https://pypi.mirrors.ustc.edu.cn/simple/


1. 官网下载Pytorch, 链接： https://pytorch.org/

    - 下载Windows Pytorch版本，官网下拉获取下载命令
        - Stable -> Windows -> Pip -> Python -> CUDA XX.X
        - Stable -> Windows -> Conda -> Python -> CPU

    - 在Anaconda Prompt中输入命令安装Pytorch-GPU(两种命令cuda 11.8示例，后面加清华源加速)
```shell
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 -i https://pypi.tuna.tsinghua.edu.cn/simple

conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
```

## Ubuntu 系统下配置 Pytorch-GPU环境


## 参考内容

1. [全网最详细的安装pytorch GPU方法，一次安装成功!!包括安装失败后的处理方法!](https://blog.csdn.net/qlkaicx/article/details/134577555)
2. [【Python】Anaconda以及Pip配置清华镜像源](https://blog.csdn.net/weixin_44914727/article/details/130513081)
3. [Linux系统安装Anaconda3保姆级教程](https://blog.csdn.net/arno_an/article/details/105229780#:~:text=%E6%95%B4%E7%90%86%E4%B8%80%E4%B8%8BAn)