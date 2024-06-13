# 注册
通过[https://app.getgrass.io/register/?referralCode=u4_ZuGVqm3drGWM](https://app.getgrass.io/register/?referralCode=u4_ZuGVqm3drGWM)
[Grass: Earn a Stake in the AI Revolution](https://app.getgrass.io/register/?referralCode=u4_ZuGVqm3drGWM)
来注册账户（在注册的过程中需要开代理 因为有一个Google验证码，该验证码在国内无法加载）
# 安装
## Mac/Linux环境
### 从GitHub仓库clone源代码
`git clone [https://github.com/David-xian66/getGrass_Xian.git](https://github.com/David-xian66/getGrass_Xian.git)`
### 安装python3
一般Linux环境自带python3 本程序最低支持python3.8
Mac环境的python3安装我们这里直接略过
### 安装依赖
在终端执行`pip3 install websockets`来安装依赖项
### 启动挖矿
通过终端执行`./start.sh`或者`python3 main.py`来执行项目
### 添加开机自启
Linux环境这里直接省略，都用Linux了还不会开机自启的话你也没必要用Linux了
Mac系统打开系统设置，找到用户与群组设置
![a59cde4ddd0e8d54e5fae019faa40032.png](https://cdn.nlark.com/yuque/0/2024/png/29245167/1718297476630-84ee81d1-56ae-4c95-b7c4-090eb3904288.png#averageHue=%23262726&clientId=u2b55cb06-fabc-4&from=paste&height=500&id=u0169d836&originHeight=500&originWidth=668&originalType=binary&ratio=1&rotation=0&showTitle=false&size=60761&status=done&style=none&taskId=ud7ab6dd1-6e71-43b1-a354-32b0070d029&title=&width=668)
点击+号，添加start.sh文件进入开机自启。![eaaa5ccf92e9c46bd209b6724761972a.png](https://cdn.nlark.com/yuque/0/2024/png/29245167/1718297846416-56342fc8-7097-4772-b9cc-3dbed991c3d6.png#averageHue=%23262726&clientId=ue15bf249-d6a0-4&from=paste&height=500&id=ua26b6216&originHeight=500&originWidth=668&originalType=binary&ratio=1&rotation=0&showTitle=false&size=63619&status=done&style=none&taskId=ued729257-677e-451b-8b3b-15ab954b5a1&title=&width=668)

ps：这里展示的是最简单的添加过程，至于如何通过`.plist文件`在用户未登录电脑但电脑已启动的情况下运行挖矿，以及通过`.plist文件`为挖矿进程配置系统级别的进程异常退出保护这里不一一赘述

## Windows环境
### 下载安装包（通过群文件或者[GitHub仓库](https://github.com/David-xian66/getGrass_Xian/releases)下载）
### 安装
#### 脚本安装
以管理员权限运行`install.exe`
该脚本会自动安装在`ProgramFiles(x86)/Seewo/seewo`目录下，同时通过Windows自动任务程序添加开机自启
#### 手动安装
手动复制安装包目录下的`install_dir`目录下的所有内容到你想安装的位置
之后自己添加开机自启等内容

# 修改配置
## 打开浏览器的开发者工具
在浏览器上打开grass控制台，登录之后打开浏览器的开发者工具。
通过浏览器右键或者直接点击F12来打开工具
![fa2abc804f521359c46b56419a46066e.png](https://cdn.nlark.com/yuque/0/2024/png/29245167/1718298389706-e151018d-0a59-4713-9f6d-4b5db160492f.png#averageHue=%232c3236&clientId=ufa1ded3d-b6da-4&from=paste&height=357&id=uf260b0d6&originHeight=357&originWidth=258&originalType=binary&ratio=1&rotation=0&showTitle=false&size=90832&status=done&style=none&taskId=u93c0246e-493a-4886-8c75-0fcd0e2b3a9&title=&width=258)
## 获取自己账户的`user_id`
在开发者工具中的控制台中输入`localStorage.getItem('userId')`，回车后复制得到的值
![24d66d562006db724962e834cfa68aea.png](https://cdn.nlark.com/yuque/0/2024/png/29245167/1718298602842-8edbe76c-a6b4-4588-95e8-662993475284.png#averageHue=%23322f2d&clientId=ufa1ded3d-b6da-4&from=paste&height=640&id=u98bd30c8&originHeight=640&originWidth=1008&originalType=binary&ratio=1&rotation=0&showTitle=false&size=167404&status=done&style=none&taskId=ufef6c9ca-ce65-49e3-af42-c3662be58b7&title=&width=1008)

## 更改项目中的`**user_id**`**为你自己账户的**`**user_id**`
### Windows环境
进入安装目录，用笔记本等工具打开`seewo.dll`，修改这里的值为你自己账户的`user_id`
![b8b07367de5080ca5c52b6a7936fb082.png](https://cdn.nlark.com/yuque/0/2024/png/29245167/1718298834255-62b3b46a-3ff0-4272-8696-e5190da10750.png#averageHue=%232b2a29&clientId=ufa1ded3d-b6da-4&from=paste&height=418&id=u43f7930c&originHeight=418&originWidth=682&originalType=binary&ratio=1&rotation=0&showTitle=false&size=88537&status=done&style=none&taskId=ufeaede71-5927-492e-bdaf-141cff1f3f8&title=&width=682)
### Mac/Linux环境
和Windows环境一样，只是直接去安装目录下找`main.py`，修改的方式和Windows一样
