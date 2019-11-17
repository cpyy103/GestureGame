import cv2
from test import predict_gesture_img, predict_face_img

face_cascade = cv2.CascadeClassifier(r'./haarcascade_frontalface_default.xml')

color = (255, 0, 0)


def gesture_detect(image):
    cv2.rectangle(image, (420, 200), (640, 420), color, 2)
    cut = cv2.cvtColor(image[200: 420, 420: 640], cv2.COLOR_BGR2RGB)
    result = predict_gesture_img(cut)
    cv2.putText(image, result, (420, 190), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    return result, image


def gesture_main():
    cap = cv2.VideoCapture(0)
    while True:
        ret, img = cap.read()
        pre, img = gesture_detect(img)
        cv2.imshow('result', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


# 只检测一张人脸
def face_detect_1(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=5, minSize=(5, 5))

    if len(faces) == 0:
        return 'UnKnow', image

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
        x1 = max(int(x - 0.2 * w), 0)
        y1 = max(int(y - 0.3 * h), 0)
        x2 = min(int((x + w) * 1.05), image.shape[1])
        y2 = min(int((y + h) * 1.1), image.shape[0])

        cut = cv2.resize(image[y1:y2, x1:x2], (224, 224))
        cut = cv2.cvtColor(cut, cv2.COLOR_BGR2RGB)
        result = predict_face_img(cut)
        cv2.putText(image, result, (x + w, y + h), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    # cv2.imshow('result', image)
        return result, image


def face_main():
    cap = cv2.VideoCapture(0)
    while True:
        ret, img = cap.read()
        pre, img = face_detect_1(img)
        cv2.imshow('result', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def main():
    cap = cv2.VideoCapture(0)
    while True:
        ret, img = cap.read()
        _, img = face_detect_1(img)
        _, img = gesture_detect(img)
        cv2.imshow('result', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # gesture_main()
    # face_main()
    main()




