# Git Note

[TOC]

## Basic git

1. Make sure your local copy of the selected branch is updated.
   1. Without overwriting anything
      1. fetch down all the branches from that Git remote
         - `git fetch [alias]`
      1. merge a remote branch into your current branch to bring it up to date
         - `git merge [alias]/[branch]`
   2. If you already fetched or you are ready to **overwrite your local copy**, (fetch and merge any commits from the tracking remote branch), then pull
      - **`git pull [alias] [branch]`**
      - **`git pull origin [branch]`**

2. Check your repo branches
   1. Local branches
      - `git branch`
   2. All branches on remote repo
      - `git branch -r`
   3. Both local and remote branches
      - `git branch -a`
   4. You can also add `-v` to make the commands explicitly verbose
3. Create a branch and access it
   1. Normal way
      1. create a new branch at the current commit
         - `git branch [new_branch]`
      2. switch to another branch and check it out into your working directory(2 ways)
         - `git checkout [new_branch]`
         - `git switch new_branch`  > Recommended option (avoid `checkout` unless necessary)
   2. Shortcut (2 ways)
      - `git checkout -b [new_branch]`
      - `git switch -c [new_branch]` > Recommended option (avoid `checkout` unless necessary)
4. Get some work done lol
5. Check the status of your work
   - `git status`
6. Did you mess up editing a file and want to restore it to how it was beforehand?
   - `git restore changed_file.txt`
7. Add changes to staging in order to prepare your commit
   1. Add a single file
      - `git add [new_file]`
   2. Add all changed files
      - **`git add . -p`**
8. Did you screw up? Reset the staging
   - `git reset`
9. Commit
   - **`git commit -m "[This is a commit message]"`**

10. Check the commit history of the current branch you're in
    - **`git log`**
    - If you wanna see some cool things with log, you can use something like this:
      - `git log --graph --oneline --all`

11. Make sure you upload your commits to the remote repo! If your local branch is brand new, you must add it to the remote repo.
    1. New branch (Transmit local branch commits to the remote repository branch)
       - **`git push -u origin new_branch`**
    2. Previously existing branch
       - `git push [alias] [branch]`
12. Move to another branch
    - `git checkout another_branch`
13. Merge some branch into your current branch (assuming default behavior of pull is merge)
    - `git pull branch_that_will_be_merged_into_current_branch`

For more info check the [GitHub Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

## Official method

_[Reference1:Git-on-the-Server-Getting-Git-on-a-Server](https://git-scm.com/book/en/v2/Git-on-the-Server-Getting-Git-on-a-Server)_
_[Reference2:create-a-remote-git-repo-from-local-folder](https://stackoverflow.com/questions/14087667/create-a-remote-git-repo-from-local-folder)_

## A concise operation of Github

_Reference Source: [GitHub初学——上传、修改本地项目文件到GitHub](https://blog.csdn.net/Demonslzh/article/details/104268334)_

1. 首先打开一个GitHub的Repository（或者新建一个，新建repository的按钮打开主页可以直接看到）
2. 回到本地，打开我们的项目所在文件
   - 点击右键，选择Git Bash Here
   - 输入`git init`，初始化本地仓库
   - `git clone https://github.com/username/repository.git`，将远程仓库克隆到本地
   - `cd repository` 进入仓库
3. 修改并上传项目
   - 如果是第二次或第三次上传，`git pull origin main`
   - `git add .`，添加所有文件
   - `git commit -m "message"`， 提交修改注释
   - `git push -u origin main`， 上传到远程仓库
4. 其他操作
   - `ssh -T git@github.com`，测试连接， 如果成功连接到github会看到如下的输出: <p>`Hi YongDeng715! You've successfully authenticated, but GitHub does not provide shell access.`</p>

Github 如何连接上电脑或服务器：
window电脑可以下载 git portable 软件，

使用 SSH 代替 HTTPS 进行验证的步骤：
1. 生成 SSH 密钥: 
```bash
   ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```
2. 添加 SSH 密钥到 SSH 代理：
```bash
   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/id_rsa
```
3. 复制公钥内容，将公钥添加到 Github:
   ```cat ~/.ssh/id_rsa.pub```
4. `ssh -T git@github.com`，测试连接， 如果成功连接到github会看到如下的输出: <p>`Hi YongDeng715! You've successfully authenticated, but GitHub does not provide shell access.`</p>

GPG 密钥用于签署和验证 Git 提交的真实性。以下是生成 GPG 密钥并配置 Git 以使用 GPG 密钥的方法：
1. 确保系统上安装了GPG， 如果没有安装，可以采用以下命令：
   ```bash
   sudo apt-get install gnupg # in Ubuntu/Debian platform
   brew install gnupg # in macOS platform
   ```
2. 生成 GPG 密钥 ```gpg --full-generate-key```
   根据提示选择密钥类型、大小和有效期，并提供你的用户信息（如姓名和电子邮件）。例如：
      - 类型：RSA and RSA (default)
      - 密钥大小：4096
      - 有效期：0（表示永不过期）
      - 用户信息：输入你的姓名和电子邮件`
3. 列出 GPG 密钥： ```gpg --list-secret-keys --keyid-format LONG```
   可以看到类似的输出：
   ```bash
   /home/username/.gnupg/secring.gpg
   -------------------------------
   sec   4096R/ABCDEF1234567890 2024-06-18 [expires: 2025-06-18]
   uid                          Your Name <you@example.com>
   ssb   4096R/1234567890ABCDEF 2024-06-18
   ```
4. 导出你的公钥，并将其添加到 GitHub： ```gpg --armor --export ABCDEF1234567890```