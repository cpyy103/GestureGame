from gesture_data_loader import train_loader
from model import GestureModel, ResNet
import torch
import torch.nn as nn
import torch.optim as optim
from matplotlib import pyplot as plt
from config import GESTURE_MODEL_PATH, GESTURE_CLASS_NUM, FACE_MODEL_PATH, FACE_CLASS_NUM, USE_GPU


def gesture_train():
    MAX_EPOCH = 100
    LR = 0.002

    net = GestureModel(GESTURE_CLASS_NUM)
    if USE_GPU:
        net.cuda()

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=LR, momentum=0.9)
    train_curve = []
    for epoch in range(MAX_EPOCH):
        correct = 0
        loss_mean = 0
        total = 0
        net.train()
        for i, data in enumerate(train_loader):
            inputs, labels = data
            if USE_GPU:
                inputs, labels = inputs.cuda(), labels.cuda()
            outputs = net(inputs)
            optimizer.zero_grad()
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            if USE_GPU:
                correct += (predicted == labels).squeeze().sum().cpu().numpy()
            else:
                correct += (predicted == labels).squeeze().sum().numpy()
            loss_mean += loss.item()
            if (i + 1) % 50 == 0:
                loss_mean = loss_mean / 50
                train_curve.append(loss_mean)
                print('Training: Epoch [{}/{}], Iteration[{}/{}], Loss:{:.4f}, acc:{:.4f} '.format(
                    epoch + 1, MAX_EPOCH, i + 1, len(train_loader), loss_mean, correct / total))
                loss_mean = 0

    torch.save(net, GESTURE_MODEL_PATH)
    try:
        torch.save(net.state_dict(), './model/gesture2.pkl')
    except Exception as e:
        print(e)


    train_x = range(len(train_curve))
    train_y = train_curve

    plt.plot(train_x, train_y, label='Train')
    plt.legend(loc='upper right')
    plt.ylabel('loss value')
    plt.xlabel('Iteration')
    plt.show()


def face_train():
    MAX_EPOCH = 30
    LR = 0.002

    net = ResNet(FACE_CLASS_NUM)
    if USE_GPU:
        net.cuda()

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=LR, momentum=0.9)
    train_curve = []
    for epoch in range(MAX_EPOCH):
        correct = 0
        loss_mean = 0
        total = 0
        net.train()
        for i, data in enumerate(train_loader):
            inputs, labels = data
            if USE_GPU:
                inputs, labels = inputs.cuda(), labels.cuda()
            outputs = net(inputs)
            optimizer.zero_grad()
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            if USE_GPU:
                correct += (predicted == labels).squeeze().sum().cpu().numpy()
            else:
                correct += (predicted == labels).squeeze().sum().numpy()
            loss_mean += loss.item()
            if (i + 1) % 20 == 0:
                loss_mean = loss_mean / 20
                train_curve.append(loss_mean)
                print('Training: Epoch [{}/{}], Iteration[{}/{}], Loss:{:.4f}, acc:{:.4f} '.format(
                    epoch + 1, MAX_EPOCH, i + 1, len(train_loader), loss_mean, correct / total))
                loss_mean = 0

    torch.save(net, FACE_MODEL_PATH)
    try:
        torch.save(net.state_dict(), './model/face2.pkl')
    except Exception as e:
        print(e)
        print('error')

    train_x = range(len(train_curve))
    train_y = train_curve

    plt.plot(train_x, train_y, label='Train')
    plt.legend(loc='upper right')
    plt.ylabel('loss value')
    plt.xlabel('Iteration')
    plt.show()


if __name__ == '__main__':
    print('Start Training...')
    # gesture_train()
    face_train()


