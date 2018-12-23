from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys, face_dll
import face_function as fun
import face_class, cv2
from ctypes import *
app = QApplication(sys.argv)


class initform(QWidget):
    def __init__(self):
        super().__init__()
        # return self.initUI()

    def initUI(self):
        # 设置窗口左上边距,宽度高度
        self.setGeometry(300, 300, 1200, 600)
        # 设置窗体标题
        self.setWindowTitle("myui")
        # self.layout=QGridLayout(self)
        # 设置lable文本内容
        self.lable = QLabel("iamlable", self)
        # label的对其方式,为左上对其
        self.lable.setAlignment(Qt.AlignTop)
        self.lable.setAlignment(Qt.AlignLeft)
        # 设置labl的大小
        self.lable.setGeometry(0, 0, 800, 600)
        self.lable.setScaledContents(True)
        # 添加按钮
        bt1 = QPushButton('打开图片', self)
        bt1.move(810, 50)
        bt1.clicked.connect(self.bt1click)
        # 添加textbox
        self.tx1 = QLineEdit(self)
        self.tx1.move(810, 80)
        # 添加另一个图片
        self.l2 = QLabel('imlable2', self)
        self.l2.setAlignment(Qt.AlignTop)
        self.l2.setAlignment(Qt.AlignLeft)
        self.l2.setGeometry(810, 120, 320, 240)
        self.l2.setScaledContents(True)
        # tx1.setText(self,'空')
        self.show()

    def SetPic(self, img):
        self.lable.setPixmap(QPixmap.fromImage(img))

    def SetPic2(self, img):
        # self.l2.pixmap()
        self.l2.setPixmap(QPixmap.fromImage(img))

    def bt1click(self):
        fp = QFileDialog.getOpenFileName(self, '选择图片', 'd:/', '图片文件 (*.jpg)')
        # self.tx1.setText(self,str(fp))
        # print(fp)
        self.tx1.setText(fp[0])
        print(self.tx1.text())
        if fp[0] != '':
            self.showimage(self.tx1.text())
            self.gettz(fp[0])

    def showimage(self, fp):
        im = fun.LoadImgfromFP(fp)
        img = fun.mat2qimage(im.data)
        self.SetPic2(img)

    tezheng = c_void_p()

    def gettz(self, fp):
        # im=face_class.IM()
        # im.filepath=fp
        im = fun.LoadImgfromFP(fp)
        ret = fun.RLSB(im)
        ft = fun.getsingleface(ret[1], 0)
        ret = fun.RLTZ(im, ft)
        if ret[0] == 0:
            tezheng = ret[1]
            print(tezheng)
