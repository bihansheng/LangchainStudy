# 在开发Python应用程序的时候，系统安装的Python3只有一个版本：3.x。所有第三方的包都会被pip安装到Python3的site-packages目录下。

# 如果我们要同时开发多个应用程序，那这些应用程序都会共用一个Python，就是安装在系统的Python 3。如果应用A需要jinja 2.7，而应用B需要jinja 2.6怎么办？

# 这种情况下，每个应用可能需要各自拥有一套“独立”的Python运行环境。venv就是用来为一个应用创建一套“隔离”的Python运行环境。

# 首先，我们假定要开发一个新的项目project101，需要一套独立的Python运行环境，可以这么做：

# 第一步，创建目录，这里把Python虚拟运行环境命名为proj101env，因此目录名为proj101env：

