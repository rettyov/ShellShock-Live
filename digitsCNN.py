import torch
import torch.nn as nn
import numpy as np
import torchvision.transforms as transforms
import torchvision.transforms.functional as F

class ConvNet(nn.Module):
    def __init__(self):
        super(ConvNet, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(1, 8, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.layer2 = nn.Sequential(
            nn.Conv2d(8, 32, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.drop_out = nn.Dropout()
        self.fc1 = nn.Linear(7 * 7 * 32, 300)
        self.fc2 = nn.Linear(300, 12)

    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = out.reshape(out.size(0), -1)
        out = self.drop_out(out)
        out = self.fc1(out)
        out = self.fc2(out)
        return out


class DefineDidgit():
    def __init__(self):
        self.model = ConvNet()

        self.classes = ['0', '1', '2', '3', '4', '5', '6',
                   '7', '8', '9', 'comma', 'minus']

        self.MODEL_STORE_PATH = 'C:/Users/Nikita/PycharmProjects/Test0/models/conv_net_model.ckpt'
        self.model.load_state_dict(torch.load(self.MODEL_STORE_PATH))

    def Digit(self, image):
        image = self.Transforms(image)

        outputs = self.model(image)
        _, predicted = torch.max(outputs.data, 1)

        return self.classes[predicted]

    def Transforms(self, image):
        image = F.to_pil_image(image)
        transform = transforms.Compose([transforms.Resize((28, 28)),
                                        transforms.Grayscale(num_output_channels=1),
                                        transforms.ToTensor(),
                                        transforms.Normalize((0.1307,), (0.3081,))])
        img_tensor = transform(image)
        img_tensor.unsqueeze_(0)

        return img_tensor
