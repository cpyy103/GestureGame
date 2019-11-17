import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PIL import Image
from play import Ui_GAME
from main import gesture_detect, face_detect_1
from pygame import mixer
import time
import cv2
import win32com.client
import random
import threading


def playMusic():
    mixer.init()
    mixer.music.load('bgm.mp3')
    mixer.music.play()
    time.sleep(5000)
    mixer.music.stop()


class MyGame(QtWidgets.QMainWindow, Ui_GAME):
    round = 1
    leftTime = 5
    score = 0
    result = ""
    photo = None
    player = ""
    gestureList = ["scissors", "rock", "paper"]

    def __init__(self):
        super(MyGame, self).__init__()
        self.setupUi(self)
        self.startButton.setIcon(QIcon("./Resources/picture/startGame.png"))
        self.continueButton.setIcon(QIcon("./Resources/picture/startGame.png"))
        self.returnButton.setIcon(QIcon("./Resources/picture/stopGame.png"))
        self.startButton.clicked.connect(self.enterGame)
        self.continueButton.clicked.connect(self.startGameTimer)
        self.returnButton.clicked.connect(self.returnFace)
        self.continueButton.setEnabled(False)
        self.returnButton.setEnabled(False)

        self.cap = cv2.VideoCapture(0)
        self.viewTimer = QTimer(self)
        self.viewTimer.timeout.connect(self.showFace)
        self.viewTimer.start(0.0001)
        self.gameTimer = QTimer(self)
        self.gameTimer.timeout.connect(self.showProcess)
        self.robotTimer = QTimer(self)
        self.robotTimer.timeout.connect(self.showRobotGesture)
        self.speaker = win32com.client.Dispatch("SAPI.SpVoice")
        threadmusic = threading.Thread(target=playMusic)
        threadmusic.start()

    def enterGame(self):
        image = Image.fromarray(self.photo)
        image.save("./photo.jpg")
        pix = QPixmap("./photo.jpg")
        self.photoLabel.setPixmap(pix)  # 在label上显示图片
        self.photoLabel.setScaledContents(True)  # 让图片自适应label大小
        self.welcomeLabel.setText("欢迎您，" + self.getPlayerName(self.player))
        msg = "游戏开始, " + "欢迎您，" + self.getPlayerName(self.player)
        self.speaker.Speak(msg)
        self.startGameTimer()

    def getPlayerName(self, id):
        name = ""
        if id == "A":
            name = "ABC"
        elif id == "B":
            name = "BCD"
        elif id == "C":
            name = "CDE"
        elif id == "D":
            name = "DEF"
        elif id == "E":
            name = "EFG"
        else:
            name = "游客"
        return name

    def showFace(self):
        ret, self.photo = self.cap.read()  # 读取图像
        img = cv2.cvtColor(self.photo, cv2.COLOR_BGR2RGB)  # 转换图像通道
        self.photo = cv2.cvtColor(self.photo, cv2.COLOR_BGR2RGB)
        self.face_result, face_img = face_detect_1(img)
        self.player = str(self.face_result)
        x = face_img.shape[1]  # 获取图像大小
        y = face_img.shape[0]
        self.zoomscale = 1  # 图片放缩尺度
        frame = QImage(face_img, x, y, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.item = QGraphicsPixmapItem(pix)  # 创建像素图元
        self.item.setScale(self.zoomscale)
        self.scene = QGraphicsScene()  # 创建场景
        self.scene.addItem(self.item)
        self.cameraView.setScene(self.scene)  # 将场景添加至视图

    def showGesture(self):
        ret, img = self.cap.read()  # 读取图像
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转换图像通道
        self.gesture_result, img = gesture_detect(img)
        x = img.shape[1]  # 获取图像大小
        y = img.shape[0]
        self.zoomscale = 1  # 图片放缩尺度
        frame = QImage(img, x, y, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.item = QGraphicsPixmapItem(pix)  # 创建像素图元
        self.item.setScale(self.zoomscale)
        self.scene = QGraphicsScene()  # 创建场景
        self.scene.addItem(self.item)
        self.cameraView.setScene(self.scene)  # 将场景添加至视图

    def returnFace(self):
        self.startButton.setEnabled(True)
        self.continueButton.setEnabled(False)
        self.returnButton.setEnabled(False)
        self.photoLabel.clear()
        self.welcomeLabel.clear()
        self.viewTimer.stop()
        self.viewTimer.timeout.connect(self.showFace)
        self.viewTimer.start(0.0001)

    def startGameTimer(self):
        self.viewTimer.stop()
        self.viewTimer.timeout.connect(self.showGesture)
        self.viewTimer.start(0.0001)
        self.startButton.setEnabled(False)
        self.continueButton.setEnabled(False)
        self.returnButton.setEnabled(False)
        self.leftTime = 5
        self.round = 1
        self.gameTimer.start(1000)
        self.robotTimer.start(1500)

    def showRobotGesture(self):
        self.robotLabel.clear()
        robotic = QMovie("./Resources/picture/robot.gif")
        self.robotLabel.setMovie(robotic)
        self.robotLabel.setScaledContents(True)
        robotic.start()

    def showProcess(self):
        self.timeLabel.clear()
        self.timeLabel.setText("倒计时:     " + str(self.leftTime))
        self.roundLabel.clear()
        self.roundLabel.setText("Round:     " + str(self.round))

        self.leftTime = self.leftTime - 1
        if self.leftTime < 0:
            self.round = self.round + 1
            self.leftTime = 5
            robotGes = self.getRobotGesture()
            self.showPlayerRes(str(self.gesture_result))
            self.showRobotRes(str(robotGes))
            self.showBattleRes(str(self.gesture_result), str(robotGes))
        if self.round > 5:
            self.continueButton.setEnabled(True)
            self.returnButton.setEnabled(True)
            self.gameTimer.stop()
            self.score = 0
            self.scoreLabel.setText("玩家累计得分：")
            self.playerLabel.clear()

    def getRobotGesture(self):
        return random.choice(self.gestureList)

    def showPlayerRes(self, gesture):
        self.playerLabel.clear()
        pixmap = QPixmap("./Resources/picture/scissors.jpg")
        if gesture == "scissors":
            pixmap = QPixmap("./Resources/picture/scissors.jpg")
        elif gesture == "rock":
            pixmap = QPixmap("./Resources/picture/rock.jpg")
        elif gesture == "paper":
            pixmap = QPixmap("./Resources/picture/paper.jpg")
        else:
            pass
        if pixmap is not None:
            self.playerLabel.setPixmap(pixmap)  # 在label上显示图片
            self.playerLabel.setScaledContents(True)  # 让图片自适应label大小
        else:
            self.playerLabel.setText(str(gesture))

    def showRobotRes(self, gesture):
        self.robotLabel.clear()
        pixmap = None
        if gesture == "scissors":
            pixmap = QPixmap("./Resources/picture/scissors.jpg")
        elif gesture == "rock":
            pixmap = QPixmap("./Resources/picture/rock.jpg")
        elif gesture == "paper":
            pixmap = QPixmap("./Resources/picture/paper.jpg")
        else:
            pass
        if pixmap is not None:
            self.robotLabel.setPixmap(pixmap)  # 在label上显示图片
            self.robotLabel.setScaledContents(True)  # 让图片自适应label大小
        else:
            self.robotLabel.setText(str(gesture))

    def showBattleRes(self, player, robot):
        self.robotTimer.stop()
        if(player == "rock" and robot == "scissors") or(player == "scissors" and robot == "paper") or(player == "paper" and robot == "rock"):
            msg = "你赢啦！"
            self.speaker.Speak(msg)

            self.score = self.score + 1
            self.scoreLabel.setText("玩家累计得分：" + str(self.score))
            # reply = QMessageBox.information(self, '对局结果', '你赢啦！', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            infoBox = QMessageBox()  # Message Box that doesn't run
            infoBox.setIcon(QMessageBox.Information)
            infoBox.setText("你赢啦！")
            infoBox.setWindowTitle("对局结果")
            infoBox.setWindowIcon(QIcon('./Resources/picture/logo.ico'))
            infoBox.setStandardButtons(QMessageBox.Ok)
            infoBox.button(QMessageBox.Ok).animateClick(1000)  # 2秒自动关闭
            infoBox.exec_()

        elif player == robot:
            msg = "平局啦！"
            self.speaker.Speak(msg)

            #reply = QMessageBox.information(self, '对局结果', '平局', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            infoBox = QMessageBox()  # Message Box that doesn't run
            infoBox.setIcon(QMessageBox.Information)
            infoBox.setText("平局啦！")
            infoBox.setWindowTitle("对局结果")
            infoBox.setWindowIcon(QIcon('./Resources/picture/logo.ico'))
            infoBox.setStandardButtons(QMessageBox.Ok)
            infoBox.button(QMessageBox.Ok).animateClick(1000)  # 2秒自动关闭
            infoBox.exec_()
        else:
            msg = "你输啦！"
            self.speaker.Speak(msg)

            #reply = QMessageBox.information(self, '对局结果', '你输啦！', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            infoBox = QMessageBox()  # Message Box that doesn't run
            infoBox.setIcon(QMessageBox.Information)
            infoBox.setText("你输啦！")
            infoBox.setWindowTitle("对局结果")
            infoBox.setWindowIcon(QIcon('./Resources/picture/logo.ico'))
            infoBox.setStandardButtons(QMessageBox.Ok)
            infoBox.button(QMessageBox.Ok).animateClick(1000)  # 2秒自动关闭
            infoBox.exec_()
        self.scoreLabel.setText("玩家累计得分：" + str(self.score))
        self.robotTimer.start(1500)


class CommonHelper:
    def __init__(self):
        pass

    @staticmethod
    def readQss(style):
        with open(style, 'r') as f:
            return f.read()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    style = './Resources/qss/mainwindow1.qss'
    qssStyle = CommonHelper.readQss(style)

    myGame = MyGame()
    myGame.setStyleSheet(qssStyle)
    myGame.setWindowTitle("剪刀石头布")
    myGame.setWindowIcon(QIcon('./Resources/picture/logo.ico'))
    myGame.setFixedSize(myGame.width(), myGame.height())
    myGame.show()
    sys.exit(app.exec_())
