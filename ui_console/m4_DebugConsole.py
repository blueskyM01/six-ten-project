from ui_console.yanhua_debug_console import *
from ui_console.beckhoff_debug_console import *
from ui_console.tracking_debug_console import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
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

# 画矩形框跟踪调试界面类
class m4_Tracking_Debug_Console(QWidget, Ui_m4_TrackingDebug):
    def __init__(self, parent=None):
        super(m4_Tracking_Debug_Console,self).__init__(parent)
        self.setupUi(self)