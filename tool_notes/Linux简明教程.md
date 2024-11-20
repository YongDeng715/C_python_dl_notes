# Linux Concise Tutorial

- [Linux Concise Tutorial](#linux-concise-tutorial)
  - [Linux 简介](#linux-简介)
    - [文件结构](#文件结构)
    - [常用命令(必须熟记)](#常用命令必须熟记)
    - [辅助指令](#辅助指令)
  - [Linux 常用操作](#linux-常用操作)
    - [目录操作](#目录操作)
    - [文件操作命令](#文件操作命令)
    - [打包和解压命令](#打包和解压命令)
    - [网络命令](#网络命令)
  - [Vim 命令基础](#vim-命令基础)
  - [Linux Shell基础](#linux-shell基础)
  - [参考资料](#参考资料)

## Linux 简介
### 文件结构

```bash
/bin        二进制文件，系统常规命令
/boot       系统启动分区，系统启动时读取的文件
/dev        设备文件
/etc        大多数配置文件
/home       普通用户的家目录
/lib        32位函数库
/lib64      64位库
/media      手动临时挂载点
/mnt        手动临时挂载点
/opt        第三方软件安装位置
/proc       进程信息及硬件信息
/root       临时设备的默认挂载点
/sbin       系统管理命令
/srv        数据
/var        数据
/sys        内核相关信息
/tmp        临时文件
/usr        用户相关设定
```

### 常用命令(必须熟记)

> cd ls mkdir rm rmdir mv cp chmod find df tar
> touch cat vi vim

### 辅助指令

```bash
  ifconfig  --help     //查看 ifconfig 命令的用法
  man shutdown         //打开命令说明后，可按"q"键退出
  su yao               //切换为用户"yao",输入后回车需要输入该用户的密码
  exit                 //退出当前用户

# 说明：显示文件系统的磁盘使用情况
  df -h            // 一种易看的显示
  df -l            // 只显示本地磁盘
# 说明：这个命令用于显示系统当前内存的使用情况，包括已用内存、可用内存和交换内存的情况 
  free -g            //以G为单位输出内存的使用量，-g为GB，-m为MB，-k为KB，-b为字节 
  free -t            //查看所有内存的汇总

# 说明：which指令会在环境变量$PATH设置的目录里查找符合条件的文件。
  which bash             //查看指令"bash"的绝对路径

# 说明：sudo命令以系统管理者的身份执行指令，经由 sudo 所执行的指令就好像是 root 亲自执行。需要输入自己账户密码。
# 使用权限：在 /etc/sudoers 中有出现的使用者
  sudo -l                              //列出目前的权限
  $ sudo -u yao vi ~www/index.html    //以 yao 用户身份编辑  home 目录下www目录中的 index.html 文件

# 说明：uname可以显示一些重要的系统信息，例如内核名称、主机名、内核版本号、处理器类型之类的信息 
  uname -a

# 查看进程
  ps -ef         //查看所有正在运行的进程
# 结束进程
  kill pid       //杀死该pid的进程
  kill -9 pid    //强制杀死该进程   

# 快速清屏
  ctrl+l        //清屏，往上翻可以查看历史操作
```

关闭与重启系统

```bash
# (1)立刻关机
  shutdown -h now
  poweroff
# (2)两分钟后关机
  shutdown -h 2
# (1)立刻重启
  shutdown -r now 
  reboot
# (2)两分钟后重启
  shutdown -r 2 

# ssh连接服务器中断，如何让命令继续在服务器执行 
# Reference: https://blog.csdn.net/qq_34769162/article/details/107948168
# Method 1
  nohup command [Arg...] [ &]
  nohup command > myout.file 2>&1 &

  sudo apt install byobu # Ubuntu默认没有安装，需要手动安装byobu:
  byobu-enable # 一登陆就显示byobu界面
  byobu-disable # 取消一登陆就显示byobu界面

# Method 2
scree      # 创建一个screen session
screen -ls  # 列举当前screen session =```screen -list```
ctrl+a+d    # 退出当前screen session
screen -r [session] # 恢复screen session并显示期间输出 
screen -X -S [session] kill # kill某个screen session
screen -X -S [session] quit	# 彻底kill某个screen session

# Method 3: disown从系统的流程session列表中删除当前session，
# 不会收到 shell 的 SIGHUP，因此进程在bash关闭后不会被终止.
diswon your_command 
```

## Linux 常用操作

### 目录操作

```bash
  cd /                 //切换到根目录
  cd /bin              //切换到根目录下的bin目录
  cd ../               //切换到上一级目录 或者使用命令：cd ..
  cd ~                 //切换到home目录
  cd -                 //切换到上次访问的目录
  cd xx(文件夹名)       //切换到本目录下的名为xx的文件目录，如果目录不存在报错
  cd /xxx/xx/x         //可以输入完整的路径，直接切换到目标目录，输入过程中可以使用tab键快速补全

  ls                   //查看当前目录下的所有目录和文件
  ls -a                //查看当前目录下的所有目录和文件（包括隐藏的文件）
  ls -l                //列表查看当前目录下的所有目录和文件c++（列表查看，显示更多信息），与命令"ll"效果一样
  ls /bin              //查看指定目录下的所有目录和文件 
  mkdir tools          //在当前目录下创建一个名为tools的目录
  mkdir /bin/tools     //在指定目录下创建一个名为tools的目录

# 删除一个目录中的一个或多个文件或目录，如果没有使用 - r 选项，则 rm 不会删除目录
  rm 文件名              //删除当前目录下的文件
  rm -f 文件名           //删除当前目录的的文件（不询问）
  rm -r 文件夹名         //递归删除当前目录下此名的目录
  rm -rf 文件夹名        //递归删除当前目录下此名的目录（不询问）
  rm -rf *              //将当前目录下的所有目录和文件全部删除
  rm -rf /*             //将根目录下的所有文件全部删除【慎用！相当于格式化系统】

# 当parent子目录被删除后使它也成为空目录的话，则顺便一并删除
  rmdir -p parent/child/child11

  mv 当前目录名 新目录名        //修改目录名，同样适用与文件操作
  mv /usr/tmp/tool /opt       //将/usr/tmp目录下的tool目录剪切到 /opt目录下面
  mv -r /usr/tmp/tool /opt    //递归剪切目录中所有文件和文件夹
  cp /usr/tmp/tool /opt       //将/usr/tmp目录下的tool目录复制到 /opt目录下面
  cp -r /usr/tmp/tool /opt    //递归剪复制目录中所有文件和文件夹

  find /bin -name 'a*'        //查找/bin目录下的所有以a开头的文件或者目录
  pwd                         //显示当前位置路径
```

### 文件操作命令

```bash
 touch  a.txt     //在当前目录下创建名为a的txt文件（文件不存在），若文件存在，将文件时间属性修改为当前系统时间

  cat a.txt          //查看文件最后一屏内容
  less a.txt         //PgUp向上翻页，PgDn向下翻页，"q"退出查看
  more a.txt         //显示百分比，回车查看下一行，空格查看下一页，"q"退出查看
  tail -100 a.txt    //查看文件的后100行，"Ctrl+C"退出查看

  grep -i "the" demo_file              //在文件中查找字符串(不区分大小写)
  grep -A 3 -i "example" demo_text     //输出成功匹配的行，以及该行之后的三行
  grep -r "ramesh" *                   //在一个文件夹中递归查询包含指定字符串的文件

```

### 打包和解压命令

```bash
  .zi/.rar          //windows系统中压缩文件的扩展名
  .tar              //Linux中打包文件的扩展名
  .gz               //Linux中压缩文件的扩展名
  .tar.gz           //Linux中打包并压缩文件的扩展名

  tar -zcvf 打包压缩后的文件名 要打包的文件
  // 参数说明：z：调用gzip压缩命令进行压缩； c：打包文件； v：显示运行过程； f：指定文件名；
  tar -zcvf a.tar file1 file2,...      //多个文件压缩打包

  tar -zxvf a.tar                      //解包至当前目录
  tar -xvf a.tar                      //解包至当前目录（此时不调用gzip命令，-zxvf无法解压时）
  tar -zxvf a.tar -C /usr------        //指定解压的位置
  unzip test.zip             //解压*.zip文件 
  unzip -l test.zip          //查看*.zip文件的内容 
```

### 网络命令

```bash
  ifconfig              //查看网络
# 查看某IP网络连接
  ping IP        //查看与此IP地址的连接情况
  netstat -an    //查看当前系统端口
  netstat -an | grep 8080     //查看指定端口

# wget下载网路文件 
  wget http://prdownloads.sourceforge.net/sourceforge/nagios/nagios-3.2.1.tar.gz
  # 下载文件并以指定的文件名保存文件
  wget -O nagios.tar.gz http://prdownloads.sourceforge.net/sourceforge/nagios/nagios-3.2.1.tar.gz

# 说明: 使用 yum 和 rpm 安装和删除插件命令
  yum install httpd      //使用yum安装apache 
  yum update httpd       //更新apache 
  yum remove httpd       //卸载/删除apache

  rpm -ivh httpd-2.2.3-22.0.1.el5.i386.rpm      //使用rpm文件安装apache 
  rpm -uvh httpd-2.2.3-22.0.1.el5.i386.rpm      //使用rpm更新apache 
  rpm -ev httpd                                 //卸载/删除apache 

# 将本地opt目录下的data文件发送到192.168.1.101服务器的opt目录下
scp /opt/data.txt  192.168.1.101:/opt/ 
scp -r /data/x.py root@192.168.1.101:/media/datc/opt/

```

## Vim 命令基础

Study Reference:  
1. [Vim文本编辑器及其应用详解](https://c.biancheng.net/linux_tutorial/40/); 
2. [RUNOOB.COM/linux-vim](https://www.runoob.com/linux/linux-vim.html)

```bash
  vi 文件名              //打开需要编辑的文件

  --进入后，操作界面有三种模式： 命令模式（command mode）、插入模式（Insert mode）和底行模式（last line mode）
  命令模式
  -刚进入文件就是命令模式，通过方向键控制光标位置，
  -使用命令"dd"删除当前整行
  -使用命令"/字段"进行查找
  -按"i"在光标所在字符前开始插入
  -按"a"在光标所在字符后开始插入
  -按"o"在光标所在行的下面另起一新行插入
  -按"："进入底行模式
  插入模式
  -此时可以对文件内容进行编辑，左下角会显示 "-- 插入 --""
  -按"ESC"进入底行模式
  底行模式
  -退出编辑：      :q
  -强制退出：      :q!
  -保存并退出：    :wq
  
  ## 操作步骤示例 ##
  1.保存文件：按"ESC" -> 输入":" -> 输入"wq",回车     //保存并退出编辑
  2.取消操作：按"ESC" -> 输入":" -> 输入"q!",回车     //撤销本次修改并退出编辑
  ## 补充 ##
  vim +10 filename.txt                   //打开文件并跳到第10行
  vim -R /etc/passwd                     //以只读模式打开文件
```

## Linux Shell基础 

[点击此处跳转到Linux Shell基础教程](LinuxShellBasic.md) 

Study Reference:  
1. [Shell脚本：Linux Shell脚本学习指南](https://c.biancheng.net/shell/); 
2. [RUNOOB.COM/linux-shell](https://www.runoob.com/linux/linux-shell.html)

## 参考资料

1. https://c.biancheng.net/linux_tutorial/;
1. https://www.runoob.com/linux/linux-tutorial.html;

1. https://blog.csdn.net/m0_46422300/article/details/104645072  
1. https://blog.csdn.net/qq_34769162/article/details/107948168
