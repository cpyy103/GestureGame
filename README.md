# GestureGame
具有人脸识别功能的剪刀石头布小游戏 :smile:
- pytorch 1.3 
- opencv-python
- pyqt
- 实时检测人脸，手势
## 文件  

name | 作用 
:-:|:-:
start.py | 启动ui界面
main.py | 仅摄像头界面
model.py | 神经网络模型
train.py | 训练模型
test.py | 测试单张图片
get_face_img.py | 从人脸origin文件下的图片中截取人脸图片，并保存到train文件夹
get_gesture_img.py | 调用电脑摄像头获取手势图片
play.py play.ui | qt界面设计
haarcascade_frontalface_default.xml | [opencv的人脸数据](https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml)

## 注意
- 项目还需要dataset文件夹和model文件夹
    - dataset
        - face
            - origin
                - A
                - B
                - C
            - train
                - A 
                - B
                - C
            - test
        - gesture
            - origin
            - train
                - paper
                - rock
                - scissors
                - unknow
            test
    - model

- 项目中的数据集，模型需要单独获取训练
- 人脸数据需要分好类的图片，origin文件夹下子文件夹名为人名，该子文件夹里为对应图片
- 手势数据通过调用电脑摄像头获取，再人工将对应手势图片放置train对应目录下
- 运行train.py开始训练
