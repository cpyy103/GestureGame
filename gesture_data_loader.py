from torch.utils.data import DataLoader
from torchvision import transforms, datasets
from config import GESTURE_TRAIN_PATH

BATCH_SIZE = 16

train_dir = GESTURE_TRAIN_PATH
norm_mean = [0.485, 0.456, 0.406]
norm_std = [0.229, 0.224, 0.225]
train_transform = transforms.Compose([
    transforms.Resize((220, 220)),
    transforms.RandomHorizontalFlip(0.5),
    transforms.RandomRotation(20),
    transforms.ToTensor(),
    transforms.Normalize(norm_mean, norm_std)
])
test_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(norm_mean, norm_std)
])

train_set = datasets.ImageFolder(root=train_dir, transform=train_transform)
train_loader = DataLoader(dataset=train_set, batch_size=BATCH_SIZE, shuffle=True)

classes = train_set.classes
class_to_idx = train_set.class_to_idx

if __name__ == '__main__':
    print('train_set: ', len(train_set))
    print(classes)
    print(class_to_idx)
