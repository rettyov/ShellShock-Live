import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn

num_epochs = 10

transform = transforms.Compose([transforms.Resize((28,28)),
                                transforms.Grayscale(num_output_channels=1),
                                transforms.ToTensor(),
                                transforms.Normalize((0.1307,), (0.3081,))])

train_dataset = torchvision.datasets.ImageFolder(root="C:/Users/Nikita/.PyCharmCE2019.1/config/scratches/signs/train/",
                                                 transform=transform)

train_loader = torch.utils.data.DataLoader(train_dataset)

# testset = dset.ImageFolder(root='tests',transform=transform)
# testloader = torch.utils.data.DataLoader(testset, batch_size=4,shuffle=True, num_workers=2)


##################
classes = ['0', '1', '2', '3', '4', '5', '6',
           '7', '8', '9', 'comma', 'minus']

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


model = ConvNet()

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)

# Train the model
total_step = len(train_loader)
loss_list = []
acc_list = []
for epoch in range(num_epochs):
    totalAll = 0
    correctAll = 0
    for i, (images, labels) in enumerate(train_loader):
        # Run the forward pass
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss_list.append(loss.item())

        # Backprop and perform Adam optimisation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # Track the accuracy
        total = labels.size(0)
        _, predicted = torch.max(outputs.data, 1)
        # print(classes[predicted])
        correct = (predicted == labels).sum().item()
        acc_list.append(correct / total)
        totalAll += total
        correctAll += correct
        # print(i)

    print('Epoch [{}/{}], Loss: {:.4f}, Accuracy: {:.2f}%'
          .format(epoch + 1, num_epochs, loss.item(),
                  (correctAll / totalAll) * 100))

# # Save the model and plot
# MODEL_STORE_PATH = 'C:/Users/Nikita/.PyCharmCE2019.1/config/scratches/model/'
# torch.save(model.state_dict(), MODEL_STORE_PATH + 'conv_net_model.ckpt')
