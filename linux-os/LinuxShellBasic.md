# Linux Shell Basics

本篇文章主要介绍如何编写一个 Shell 脚本(简单来说就是使用 Linux 和 类Unix 系统命令行语言的执行文件)

Linux 的具体命令解释可以看前一篇文章 [Linux Concise Tutorial](Linux简明教程.md)



这里给出一个案例：这个脚本将备份指定目录中的文件，并保存为带有日期的压缩文件。

```bash
#!/bin/bash

# 定义源目录和目标目录, 获取当前日期
SOURCE_DIR="/home/user/documents"
DEST_DIR="/home/user/backup"
DATE=$(date +"%Y%m%d")

# 创建目标目录（如果不存在）
mkdir -p $DEST_DIR

# 打包源目录并命名为备份文件
tar -zcvf $DEST_DIR/backup_$DATE.tar.gz $SOURCE_DIR

# 显示备份完成信息
echo "备份完成：$DEST_DIR/backup_$DATE.tar.gz"
```

如果该文件保存为 `backup.sh`，则可以通过以下两种方式运行它：

1. 使用 `bash` 命令直接运行脚本
```bash
bash backup.sh
```

2. 将脚本文件设置为可执行文件，使用 `chmod` 命令赋予脚本执行权限，然后运行它
```bash
chmod +x backup.sh
./backup.sh
```

## Shell 脚本的基本结构

1. 注释
   - 使用 `#` 开头的行是注释，不会被执行。
   - 多行注释可以使用 : `'注释内容'` 或 `<<COMMENT ... COMMENT` 格式。
  
2. 变量
   - 定义变量时不需要 `$`，但使用变量时需要加 `$`。

```bash 
VAR="Hello"
echo $VAR
```

3. 条件判断

`if`、`else` 和 `elif` 用于条件判断

```bash
if [ $age -gt 18 ]; then
  echo "成年人"
else
  echo "未成年"
fi
```

4. 循环

`for`、`while` 循环用于执行重复任务
```bash
for i in {1..5}; do
  echo "数字：$i"
done
```