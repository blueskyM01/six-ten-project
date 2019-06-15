import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal

class m4_RectTrackingSignal(QObject):
    # 定义信号
    sendmsg = pyqtSignal(str,str)
    def __init__(self):
        super(QTypeSignal, self).__init__()

    def run(self):
        # 发射信号
        self.sendmsg.emit('first', 'second')

class m4m4_RectTrackingSolt(QObject):
    def __init__(self):
        super(QTypeSolt, self).__init__()

    # 槽对象里的槽函数
    def get(self, msg1, msg2):
        print("QSlot get msg =>" + msg1 + ' ' + msg2)