# How to use
## 1. 当跟新ui文件后
* 1.1需要在parachute_console.py加入：
    ````
    from ui_console.m4_QLabel import *
    ````
* 1.2 将self.ImageShow的声明从
    ````
    QtWidgets.QLabel(self.centralwidget)
    ````
    改为
    ````
    self.m4_ImageShow = m4_QLabel(self.centralwidget)
    ````
 ## 2. beckhoff控制器注意事项
 [beckhoff的c++转python代码](https://github.com/blueskyM01/c-_To_Python)和  
 [c++_beckhoff_project](https://github.com/blueskyM01/beckoff_python_project) `在这里面修改，上传`
 * 2.1 主要位于[m4_beckoff_python.cpp](https://github.com/blueskyM01/c-_To_Python/blob/master/m4_beckoff_python.cpp)
 