import face_class
import face_ui
from ctypes import *
import cv2
import face_function as fun
import threading
Appkey = b'****************'
SDKey = b'*******************'
# 激活
ret = fun.JH(Appkey, SDKey)
if ret == 0 or ret == 90114:
    print('激活成功:')
else:
    print('激活失败:', ret)
    pass
# 初始化
ret = fun.CSH()
if ret[0] == 0:
    print('初始化成功:')
else:
    print('初始化失败:', ret)
# 加载图片
im=fun.LoadImgfromFP('d:/3.jpg')
# im = face_class.IM()
# im.filepath = 'e:/5.jpg'
# im = fun.LoadImg(im)
print('加载图片完成:')
# 人脸识别
ret = fun.RLSB(im)
if ret[0] != 0:
    print('人脸识别失败:', ret)
    pass
else:
    print('人脸识别成功:')
# 显示人脸照片
# fun.showimg(im.data,ret[1],1)
# 提取单人1特征
ft = fun.getsingleface(ret[1], 0)
tz1 = fun.RLTZ(im, ft)[1]
# fun.writeFTFile(tz1,'d:/wxt.dat')
# 提取单人2特征
# ft=fun.getsingleface(ret[1],1)
# tz2=fun.RLTZ(im,ft)[1]
# 特征保存到文件
# fun.writeFTFile(tz1,'d:/1.dat')
# fun.writeFTFile(tz2,'d:/2.dat')
# 文件获取特征
tz = fun.ftfromfile('d:/wxt.dat')

jg = fun.BD(tz, tz1)
print(jg[1])
# 结果比对
# jg=fun.BD(tz1,tz2)
# print(jg[1])

# 图片显示在QT中
# 获取带人脸框的图片 最后参数控制,是否显示数字顺序
newim = fun.rangimg(im.data, ret[1], 1)
# 初始化QT窗体并显示
ui = face_ui.initform()
ui.initUI()
# 设置图片显示
ui.SetPic(fun.mat2qimage(newim))

th = threading.Thread(target=fun.showcamre_face, args=(ui, ))
# lock=threading.Lock()
th.start()
# fun.showcamre(ui)
face_ui.app.exec_()
# 关掉摄像头进程
fun.thstop = True
