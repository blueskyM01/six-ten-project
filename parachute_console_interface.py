import time
import numpy as np
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication
from PyQt5.QtCore import QRect, Qt, QTimer, pyqtSignal
from ui_console.parachute_console import *
import ui_console.m4_DebugConsole as m4_DebugConsole
import apprcc_rc
import cv2
import types
import p_utils

class MyMainWinow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWinow,self).__init__(parent)
        self.setupUi(self)
        self.m4_MotionState = '断电'
        self.m4_CameraState = '关闭'
        self.m4_ModeState = '手动'
        self.m4_TrackingState = '否'
        self.m4_Remainer = '无'
        self.FWVelocity = 0
        self.FYVelocity = 0
        self.DiffTime = 0
        self.m4_StateOutput(self.m4_MotionState, self.m4_CameraState, self.m4_ModeState,
                            self.m4_TrackingState, self.m4_Remainer, str(self.FWVelocity),
                            str(self.FYVelocity), str(self.DiffTime))

        self.m4_TrackWinWidth = self.m4_ImageShow.width()
        self.m4_TrackWinHeight = self.m4_ImageShow.height()
        self.m4_DetectWinWidth = self.m4_DetectImageShow.width()
        self.m4_DetectWinHeight = self.m4_DetectImageShow.height()
        # self.m4_frame = 0


        self.status = self.statusBar() # 创建状态栏
        self.status.showMessage("降落伞跟踪主程序启动中....", 5000) # 5000表示5秒后消失
        self.m4_timer = QTimer() # 初始化定时器
        self.m4_YanhuaDebug = m4_DebugConsole.m4_Yanhua_Debug_Console() #创建 研华调试界面对象
        self.m4_Yanhua_action.triggered.connect(self.m4_CallYanhuaDebugConsole) # 创建 研华调试界面对象信号槽
        self.m4_BeckHoffDebug = m4_DebugConsole.m4_BeckHoff_Debug_Console()  # 创建 倍福调试界面对象
        self.m4_BeckHoff_action.triggered.connect(self.m4_CallBeckHoffDebugConsole) # 创建 倍福调试界面对象信号槽

        self.m4_TrackingDebug = m4_DebugConsole.m4_Tracking_Debug_Console()  # 创建 跟踪调试界面对象
        self.m4_manual_tracking_action.triggered.connect(self.m4_CallTrackingDebugConsole)  # 创建 跟踪调试界面对象信号槽
        self.m4_timer.timeout.connect(self.m4_TrackingPlay) # 创建 定时器信号槽
        self.m4_open_camera_action.triggered.connect(self.m4_OpenCamera) # 创建 打开相机信号槽
        self.m4_close_camera_action.triggered.connect(self.m4_CloseCamera)  # 创建 关闭相机信号槽
        self.m4_ImageShow.sendmsg.connect(self.m4_TrackingInit)


    # 显示研华调试界面 槽函数
    def m4_CallYanhuaDebugConsole(self):
        self.m4_YanhuaDebug.show()

    # 显示倍福调试界面 槽函数
    def m4_CallBeckHoffDebugConsole(self):
        self.m4_BeckHoffDebug.show()

    # 显示跟踪调试界面 槽函数
    def m4_CallTrackingDebugConsole(self):
        self.m4_TrackingDebug.show()

    # 打开相机
    def m4_OpenCamera(self):
        if self.m4_timer.isActive() == False: # 定时器m4_timer没有启动
            self.m4_ImageShow.setEnabled(True)
            self.m4_DetectImageShow.setEnabled(True)
            self.m4_timer.start(44) # 启动定时器m4_timer
            self.capture = cv2.VideoCapture(0)  # 相机初始化
            self.m4_Remainer = '相机已打开....'
            self.m4_CameraState = '打开'
            self.m4_StateOutput(self.m4_MotionState, self.m4_CameraState, self.m4_ModeState,
                                self.m4_TrackingState, self.m4_Remainer, str(self.FWVelocity),
                                str(self.FYVelocity), str(self.DiffTime))
        else:
            self.m4_Remainer = '相机已经打开，无需再次打开....'
            self.m4_StateOutput(self.m4_MotionState, self.m4_CameraState, self.m4_ModeState,
                                self.m4_TrackingState, self.m4_Remainer, str(self.FWVelocity),
                                str(self.FYVelocity), str(self.DiffTime))


    # 关闭相机
    def m4_CloseCamera(self):
        if self.m4_timer.isActive():
            self.m4_timer.stop()
            self.capture.release()
            self.m4_ImageShow.setPixmap(QtGui.QPixmap(":/pic/IfyEzBj.jpg"))
            self.m4_DetectImageShow.setPixmap(QtGui.QPixmap(":/pic/para.png"))
            self.m4_Remainer = '相机已关闭....'
            self.m4_CameraState = '关闭'
            self.FWVelocity = 0
            self.FYVelocity = 0
            self.DiffTime = 0
            self.m4_StateOutput(self.m4_MotionState, self.m4_CameraState, self.m4_ModeState,
                                self.m4_TrackingState, self.m4_Remainer, str(self.FWVelocity),
                                str(self.FYVelocity), str(self.DiffTime))
            self.m4_ImageShow.setEnabled(False)
            self.m4_DetectImageShow.setEnabled(False)
        else:
            self.m4_Remainer = '相机已经关闭，无需再次关闭....'
            self.m4_StateOutput(self.m4_MotionState, self.m4_CameraState, self.m4_ModeState,
                                self.m4_TrackingState, self.m4_Remainer, str(self.FWVelocity),
                                str(self.FYVelocity), str(self.DiffTime))

    # 显示跟踪图像
    def m4_TrackingPlay(self):
        m4_StartTime = time.time()
        ret, self.m4_frame = self.capture.read()
        self.m4_TrackingImageShow(self.m4_frame)
        self.m4_DetectingImageShow(self.m4_frame)
        m4_EndTime = time.time()
        m4_DiffTime = (m4_EndTime - m4_StartTime) * 1000
        self.DiffTime = m4_DiffTime
        self.m4_StateOutput(self.m4_MotionState, self.m4_CameraState, self.m4_ModeState,
                            self.m4_TrackingState, self.m4_Remainer, str(self.FWVelocity),
                            str(self.FYVelocity), str(self.DiffTime))

        # print(self.m4_OutputState.verticalScrollBar().value())



    # 主窗口显示图像
    def m4_TrackingImageShow(self, frame):
        frame = frame.copy()
        height, width, bytesPerComponent = frame.shape
        bytesPerLine = 3 * width
        cv2.cvtColor(frame, cv2.COLOR_BGR2RGB, frame)
        QImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(QImg)
        self.m4_ImageShow.setPixmap(pixmap)

    # 检测窗口显示图像
    def m4_DetectingImageShow(self, frame):
        frame = frame.copy()
        height, width, bytesPerComponent = frame.shape
        bytesPerLine = 3 * width
        cv2.cvtColor(frame, cv2.COLOR_BGR2RGB, frame)
        QImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(QImg)
        self.m4_DetectImageShow.setPixmap(pixmap)

    # 在状态栏中输出状态，信息等
    def m4_StateOutput(self, m4_MotionState, m4_CameraState, m4_ModeState, m4_TrackingState, m4_Remainer,
                       FWVelocity, FYVelocity, DiffTime):

        m4_Device = "电机状态："
        m4_State = m4_MotionState
        m4_Device += "\n"
        m4_State += "\n"

        m4_Device += "相机状态："
        m4_State += m4_CameraState
        m4_Device += "\n"
        m4_State += "\n"

        m4_Device += "手|自模式："
        m4_State += m4_ModeState
        m4_Device += "\n"
        m4_State += "\n"

        # m4_Device += "是否开始目标切换跟踪:"
        # m4_State += m4_TrackingState
        # m4_Device += "\n"
        # m4_State += "\n"

        m4_OutputInfo = '方位轴速度：'
        m4_OutputInfo += FWVelocity
        m4_OutputInfo += ' °/s'
        m4_OutputInfo += '\n'
        m4_OutputInfo += '俯仰轴速度：'
        m4_OutputInfo += FYVelocity
        m4_OutputInfo += ' °/s'
        m4_OutputInfo += '\n'
        m4_OutputInfo += '程序执行时间：'
        m4_OutputInfo += DiffTime
        m4_OutputInfo += '\n'

        m4_Remaind = "提示："
        m4_RemaindInfo = m4_Remainer

        self.m4_OutputState.setText(m4_Device)
        self.m4_State.setText(m4_State)
        self.m4_OutputInfo.setText(m4_OutputInfo)

        self.m4_OutputRemainder.setText(m4_Remaind)
        self.m4_Remainder.setText(m4_RemaindInfo)


    def m4_TrackingInit(self, x0, y0, x1, y1):
        print(self.m4_TrackWinWidth, self.m4_TrackWinHeight)
        m4_xtl, m4_ytl, m4_xbr, m4_ybr = p_utils.m4_CoordinateConvert(x0, y0, x1, y1,
                                                                      self.m4_TrackWinWidth, self.m4_TrackWinHeight,
                                                                      self.m4_frame.shape[1], self.m4_frame.shape[0])
        cv2.rectangle(self.m4_frame, (m4_xtl, m4_ytl), (m4_xbr, m4_ybr), (0, 0, 255), 5)
        cv2.imwrite('dddd.png',self.m4_frame)







if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMainWinow()
    myWin.show()
    sys.exit(app.exec())