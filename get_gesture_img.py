# 调用摄像头截取手势图片
import cv2
import time


cap = cv2.VideoCapture(0)
print(cap.get(3))
print(cap.get(4))
left_top = (420, 200)  # 根据摄像头调试， 我的是640*480
right_bottom = (640, 420)
color = (0, 255, 0)
thickness = 2

# cap.set(3, 640)#视频每一帧的宽
# cap.set(4, 480)#视频每一帧的高
# print(cap.get(cv2.CAP_PROP_FPS))
i = 0
while True:
    i += 1
    ret, img = cap.read()
    cv2.rectangle(img, left_top, right_bottom, color, thickness)
    cv2.imshow('result', img)
    cut = img[200: 420, 420: 640]
    time.sleep(0.3)
    cv2.imwrite('./dataset/gesture/origin/' + str(i) + '.jpg', cut)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
