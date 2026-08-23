import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

# Define a transform to normalise the data
transform = transforms.Compose(
    [transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))]
)

# Download and load the MNSIT Dataset
train_data = datasets.MNIST(
    root="./data", train=True, download=True, transform=transform
)

# Download and load the test data
test_data = datasets.MNIST(
    root="./data", train=False, download=True, transform=transform
)

# Wrap in DataLoaders
train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = DataLoader(test_data, batch_size=64, shuffle=False)

print(f"Training samples: {len(train_data)}")
print(f"Test samples: {len(test_data)}")


## Define the Model ##
class SimpleNetwork(nn.Module):
    def __init__(self):
        super(SimpleNetwork, self).__init__()
        self.fc1 = nn.Linear(784, 128)  # 28x28 = 784 input pixels
        self.fc2 = nn.Linear(128, 64)  # hidden layer
        self.fc3 = nn.Linear(64, 10)  # 10 outputs (digits 0-9)

    def forward(self, x):
        x = x.view(-1, 784)  # flatten the image
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


model = SimpleNetwork()
print(model)

## Train the model ##
# Define loss function and optimizer
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Training loop
epochs = 5

for epoch in range(epochs):
    model.train()
    running_loss = 0

    for images, labels in train_loader:
        # Forward pass
        predictions = model(images)
        loss = loss_fn(predictions, labels)

        # Backward pass (Backpropagation)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    avg_loss = running_loss / len(train_loader)
    print(f"Epoch {epoch+1}/5 — Loss: {avg_loss:.4f}")

## Model evaluation ##
model.eval()
correct = 0
total = 0

with torch.no_grad():
    for images, labels in test_loader:
        predictions = model(images)
        _, predicted = torch.max(predictions, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

accuracy = 100 * correct / total
print(f"Test Accuracy: {accuracy:.2f}%")
