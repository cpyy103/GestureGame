"""从origin文件夹现有的照片中截取出人脸并保存"""
import os
import cv2
import random

face_cascade = cv2.CascadeClassifier(r'./haarcascade_frontalface_default.xml')


def face_detect(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=5, minSize=(5, 5))
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
    cv2.imshow('result', image)


def makedir(new_dir):
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)


def get_face_data(origin_path, train_path):
    count = 1
    for root, dirs, files in os.walk(origin_path):
        for d in dirs:
            imgs = os.listdir(os.path.join(root, d))
            random.shuffle(imgs)

            for img in imgs:
                img = cv2.imread(os.path.join(root, d, img))
                faces = face_cascade.detectMultiScale(img, scaleFactor=1.15, minNeighbors=5, minSize=(5, 5))
                for (x, y, w, h) in faces:
                    if w > 90 and h > 90:
                        image_name = str(count) + '.jpg'
                        count += 1
                        x1 = max(int(x - 0.2*w), 0)
                        y1 = max(int(y - 0.3*h), 0)
                        x2 = min(int((x+w)*1.05), img.shape[1])
                        y2 = min(int((y+h)*1.1), img.shape[0])

                        f = cv2.resize(img[y1:y2, x1:x2], (224, 224))
                        out_dir = os.path.join(train_path, d)
                        makedir(out_dir)
                        cv2.imwrite(os.path.join(out_dir, image_name), f)


if __name__ == '__main__':
    get_face_data('./dataset/face/origin', './dataset/face/train')
    print('Done!')