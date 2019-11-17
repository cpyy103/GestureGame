import torch
USE_GPU = torch.cuda.is_available()

GESTURE_MODEL_PATH = './model/gesture.pkl'
GESTURE_TRAIN_PATH = './dataset/gesture/train'
GESTURE_CLASS_NUM = 4

FACE_MODEL_PATH = './model/face.pkl'
FACE_TRAIN_PATH = './dataset/face/train'
FACE_CLASS_NUM = 6



