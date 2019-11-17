import gesture_data_loader
import face_data_loader
from PIL import Image
import torch
from config import GESTURE_MODEL_PATH, GESTURE_CLASS_NUM, FACE_MODEL_PATH, FACE_CLASS_NUM,USE_GPU
from model import GestureModel, ResNet

gesture_model = GestureModel(GESTURE_CLASS_NUM)
face_model = ResNet(FACE_CLASS_NUM)
if USE_GPU:
    gesture_model.load_state_dict(torch.load(GESTURE_MODEL_PATH, map_location=lambda storage, loc: storage.cuda()))
    face_model.load_state_dict(torch.load(FACE_MODEL_PATH, map_location=lambda storage, loc: storage.cuda()))
else:
    gesture_model.load_state_dict(torch.load(GESTURE_MODEL_PATH))
    face_model.load_state_dict(torch.load(FACE_MODEL_PATH))

gesture_model.eval()
face_model.eval()


def predict_gesture_img(image):
    image = gesture_data_loader.test_transform(image)
    image = image.unsqueeze(0)

    val, predicted = torch.max(gesture_model(image).data, 1)
    if val.item() > 0.5:
        return gesture_data_loader.classes[predicted.item()]
    else:
        return 'UnKnow'


def predict_face_img(image):
    image = face_data_loader.test_transform(image)
    image = image.unsqueeze(0)

    val, predicted = torch.max(face_model(image).data, 1)
    if val.item() > 0.5:
        return face_data_loader.classes[predicted.item()]
    else:
        return 'UnKnow'


if __name__ == '__main__':
    test_file = './dataset/gesture/test/36.jpg'
    img = Image.open(test_file).convert('RGB')
    print(predict_gesture_img(img))

    test_file = './dataset/face/test/69.jpg'
    img = Image.open(test_file).convert('RGB')
    print(predict_face_img(img))




