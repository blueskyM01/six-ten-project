from ui_console.yanhua_debug_console import *
from ui_console.beckhoff_debug_console import *
from ui_console.tracking_debug_console import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
import time

import c_Plus.m4_beckoff as m4_beckoff
# from c_Plus.m4_beckoff import * # 导入全部类方法
# 研华调试界面类
class m4_Yanhua_Debug_Console(QWidget, Ui_m4_YanhuaDebug):
    def __init__(self, parent=None):
        super(m4_Yanhua_Debug_Console,self).__init__(parent)
        self.setupUi(self)

# 倍福调试界面类
class m4_BeckHoff_Debug_Console(QWidget, Ui_m4_BeckHoffDebug):
    def __init__(self, parent=None):
        super(m4_BeckHoff_Debug_Console,self).__init__(parent)
        self.setupUi(self)
        self.beckoff = m4_beckoff.m4_beckhoff("Kobe Bryant", 88, 100) # 定义倍福控制类
        self.beckoff.m4_beckhoff_Init() # 倍福控制器初始化
        self.m4_FWEnableBtn.clicked.connect(self.m4_EnableFW) # 方位轴上电信号槽
        self.m4_FYEnableBtn.clicked.connect(self.m4_EnableFY) # 俯仰轴上电信号槽
        self.m4_FWDisenableBtn.clicked.connect(self.m4_DisenableFW) # 方位轴断电信号槽
        self.m4_FYDisenableBtn.clicked.connect(self.m4_DisenableFY) # 俯仰轴断电信号槽

    # 方位轴上电
    def m4_EnableFW(self):
        self.beckoff.m4_SetFWEnable(1) # 1：使能； 2：失能
        self.beckoff.m4_EnableFWAixs() # 写入控制器
        self.m4_GetEnableFWFlag()

    # 俯仰轴上电
    def m4_EnableFY(self):
        self.beckoff.m4_SetFYEnable(1) # 1：使能； 2：失能
        self.beckoff.m4_EnableFYAixs() # 写入控制器
        self.m4_GetEnableFYFlag()

    # 方位轴断电
    def m4_DisenableFW(self):
        time.sleep(0.3)
        self.beckoff.m4_SetFWEnable(0) # 1：使能； 2：失能
        self.beckoff.m4_EnableFWAixs() # 写入控制器
        self.m4_GetEnableFWFlag()

    # 俯仰轴断电
    def m4_DisenableFY(self):
        time.sleep(0.3)
        self.beckoff.m4_SetFYEnable(0) # 1：使能； 2：失能
        self.beckoff.m4_EnableFYAixs() # 写入控制器
        self.m4_GetEnableFYFlag()

    # 获取方位轴使能标志位
    def m4_GetEnableFWFlag(self):
        FWEnableFlag = self.beckoff.m4_GetFWEnable()
        self.m4_FWEnableFlag_T.setText(str(FWEnableFlag))

    # 获取俯仰轴使能标志位
    def m4_GetEnableFYFlag(self):
        FYEnableFlag = self.beckoff.m4_GetFYEnable()
        self.m4_FYEnableFlag_T.setText(str(FYEnableFlag))



# 画矩形框跟踪调试界面类
class m4_Tracking_Debug_Console(QWidget, Ui_m4_TrackingDebug):
    def __init__(self, parent=None):
        super(m4_Tracking_Debug_Console,self).__init__(parent)
        self.setupUi(self)