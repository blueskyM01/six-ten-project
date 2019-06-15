# How to use
## 1. 当跟新ui文件后
### 1.1需要在parachute_console.py加入：
````
from ui_console.m4_QLabel import *
````
### 1.2 将self.ImageShow的声明从
````
QtWidgets.QLabel(self.centralwidget)
````
改为
````
self.m4_ImageShow = m4_QLabel(self.centralwidget)
````