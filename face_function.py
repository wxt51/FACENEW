import face_dll as face_dll
import face_class
from ctypes import *
import time
import cv2
from io import BytesIO
from PyQt5.QtGui import QImage
import threading
lock = threading.Lock()
Handle = c_void_p()
c_ubyte_p = POINTER(c_ubyte)
thstop = False


# 激活函数
def JH(appkey, sdkey):
    ret = face_dll.jihuo(appkey, sdkey)
    return ret


# 初始化函数
# 1：视频或图片模式,2角度,3最小人脸尺寸推荐16,4最多人脸数最大50,5功能,6返回激活句柄
def CSH():
    ret = face_dll.chushihua(0xFFFFFFFF, 0x1, 16, 50, 5, byref(Handle))
    # Main.Handle=Handle
    return ret, Handle


# cv2加载图片并处理
def LoadImgfromFP(FP):
    img = cv2.imread(FP)
    return (LoadImageFromMat(img))


# 从摄像头获取图片
def LoadImageFromMat(img):
    im = face_class.IM()
    img = cv2.resize(img, (img.shape[1] // 4 * 4, img.shape[0] // 4 * 4))
    im.data = img.copy()
    im.width = img.shape[1]
    im.height = img.shape[0]
    return im


# 人脸识别,入参图片
def RLSB(im):
    faces = face_class.ASF_MultiFaceInfo()
    # img = im.data
    imgby = bytes(im.data)
    imgcuby = cast(imgby, c_ubyte_p)
    lock.acquire()
    ret = face_dll.shibie(Handle, im.width, im.height, im.format, imgcuby,
                          byref(faces))
    lock.release()
    return ret, faces


# 显示人脸识别图片
def showimg(im, faces, shownum=1):
    im1 = im.copy()
    font = cv2.FONT_HERSHEY_SIMPLEX
    for i in range(0, faces.faceNum):
        ra = faces.faceRect[i]
        cv2.rectangle(im1, (ra.left1, ra.top1), (ra.right1, ra.bottom1), (
            255,
            0,
            0,
        ), 2)
        if shownum == 1:
            im1 = cv2.putText(im1, str(i + 1), (ra.left1, ra.top1 - 5), font,
                              0.8, (255, 0, 0), 2)
    cv2.imshow('faces', im1)
    cv2.waitKey(0)


# 显示人脸识别图片
def rangimg(im, faces, shownum=1):
    im1 = im.copy()
    font = cv2.FONT_HERSHEY_SIMPLEX
    for i in range(0, faces.faceNum):
        ra = faces.faceRect[i]
        cv2.rectangle(im1, (ra.left1, ra.top1), (ra.right1, ra.bottom1), (
            255,
            0,
            0,
        ), 2)
        if shownum == 1:
            im1 = cv2.putText(im1, str(i + 1), (ra.left1, ra.top1 - 5), font,
                              0.8, (255, 0, 0), 2)
    return im1


# 提取人脸特征
def RLTZ(im, ft):
    detectedFaces = face_class.ASF_FaceFeature()
    # img = im.data
    imgby = bytes(im.data)
    imgcuby = cast(imgby, c_ubyte_p)
    ret = face_dll.tezheng(Handle, im.width, im.height, im.format, imgcuby, ft,
                           byref(detectedFaces))
    if ret == 0:
        retz = face_class.ASF_FaceFeature()
        retz.featureSize = detectedFaces.featureSize
        # 必须操作内存来保留特征值,因为c++会在过程结束后自动释放内存
        retz.feature = face_dll.malloc(detectedFaces.featureSize)
        face_dll.memcpy(retz.feature, detectedFaces.feature,
                        detectedFaces.featureSize)
        # print('提取特征成功:',detectedFaces.featureSize,mem)
        return ret, retz
    else:
        return ret


# 特征值比对,返回比对结果
def BD(tz1, tz2):
    jg = c_float()
    ret = face_dll.bidui(Handle, tz1, tz2, byref(jg))
    return ret, jg.value


# 单人特征写入文件
def writeFTFile(feature, filepath):
    f = BytesIO(string_at(feature.feature, feature.featureSize))
    a = open(filepath, 'wb')
    a.write(f.getvalue())
    a.close()


# 从多人中提取单人数据
def getsingleface(singleface, index):
    ft = face_class.ASF_SingleFaceInfo()
    ra = singleface.faceRect[index]
    ft.faceRect.left1 = ra.left1
    ft.faceRect.right1 = ra.right1
    ft.faceRect.top1 = ra.top1
    ft.faceRect.bottom1 = ra.bottom1
    ft.faceOrient = singleface.faceOrient[index]
    return ft


# 从文件获取特征值
def ftfromfile(filepath):
    fas = face_class.ASF_FaceFeature()
    f = open(filepath, 'rb')
    b = f.read()
    f.close()
    fas.featureSize = b.__len__()
    fas.feature = face_dll.malloc(fas.featureSize)
    face_dll.memcpy(fas.feature, b, fas.featureSize)
    return fas


# mat to qimage
def mat2qimage(ima):
    lock.acquire()
    newim = ima.copy()
    newim = cv2.cvtColor(newim, cv2.COLOR_RGB2BGR)
    newim = QImage(newim, newim.shape[1], newim.shape[0], QImage.Format_RGB888)
    lock.release()
    return newim


def cutpic(im, tezheng):
    img = im.copy()
    img = img[tezheng.faceRect.top1:tezheng.faceRect.bottom1, tezheng.faceRect.
              left1:tezheng.faceRect.right1]
    return img


def showcamre_face(ui):
    cap = cv2.VideoCapture(0)
    # 设置显示分辨率和FPS ,不设置的话会非常卡
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
    cap.set(cv2.CAP_PROP_FPS, 20)
    while cap.isOpened():
        if thstop:
            return
        ret, frame = cap.read()
        if not ret:
            continue
        else:
            pass
        # 水平翻转,很有必要
        frame = cv2.flip(frame, 1)
        frame1 = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        im = LoadImageFromMat(frame)
        ret = RLSB(im)
        # newim=None
        if ret[0] == 0:
            # 识别成功 人头>0则显示
            if ret[1].faceNum > 0:
                drtz = getsingleface(ret[1], 0)
                ctim = cutpic(frame1, drtz)
                # 偶尔崩溃,由于按倍数缩放造成,添加判断
                if ctim.shape[1] > 4 and ctim.shape[0] > 4:
                    ctim1 = LoadImageFromMat(ctim).data
                    aa = QImage(ctim1.data, ctim1.shape[1], ctim1.shape[0],
                                QImage.Format_RGB888)
                    ui.SetPic2(aa)
            newim = rangimg(frame1, ret[1], 1)

            # opencv 默认图像格式是rgb qimage要使用BRG,这里进行格式转换,不用这个的话,图像就变色了
            a = QImage(newim.data, newim.shape[1], newim.shape[0],
                       QImage.Format_RGB888)
            # print(a)
            ui.SetPic(a)
        else:
            a = QImage(frame1.data, frame.shape[1], frame.shape[0],
                       QImage.Format_RGB888)
            ui.SetPic(a)
            ui.SetPic2(None)
        time.sleep(0.02)


def GettzFrommat(im, index):
    clim = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
    fh = GettzFromim(clim, index)
    if fh[0] != 0:
        return 0, 0
    return fh


def GettzFromim(im, index):
    frame = LoadImageFromMat(im)
    sb = RLSB(frame)
    if sb[0] != 0:
        return 0, 0
    tz = getsingleface(sb[1], index)
    if tz[0] != 0:
        return 0, 0
    ret = RLTZ(frame, tz)
    if ret[0] != 0:
        return 0, 0
    return 0, ret[1]


def GettzfromFile(path, index):
    pass


def GetJGfromIM(im1, im2):
    pass


def GetJGFromFile(path1, path2):
    pass
