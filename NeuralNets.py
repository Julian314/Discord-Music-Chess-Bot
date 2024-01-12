import torch
import torch.nn as nn

class NeuralNetwork(nn.Module):
  def __init__(self, input_size, layer_sizes):
    super(NeuralNetwork, self).__init__()

    layers = []
    for i in range(len(layer_sizes) - 1):
      layers.append(nn.Linear(layer_sizes[i], layer_sizes[i+1]))
      layers.append(nn.ReLU())

      # Remove the last ReLU to avoid an activation after the final layer
      layers.pop()

      self.seq = nn.Sequential(*layers)

  def forward(self, x):
    return self.seq(x)

class NeuralNetwork_OG(nn.Module):
  def __init__(self):
    super().__init__()
    self.fc1 = nn.Linear(800, 128)
    self.relu1 = nn.ReLU()
    self.fc2 = nn.Linear(128, 64)
    self.relu2 = nn.ReLU()
    self.fc3 = nn.Linear(64,32)
    self.relu3 = nn.ReLU()
    self.fc4 = nn.Linear(32,16)
    self.relu4 = nn.ReLU()
    self.output_layer = nn.Linear(16,1)

  def forward(self, x):
    x = self.fc1(x)
    x = self.relu1(x)
    x = self.fc2(x)
    x = self.relu2(x)
    x = self.fc3(x)
    x = self.relu3(x)
    x = self.fc4(x)
    x = self.relu4(x)
    x = self.output_layer(x)

    return x

class NeuralNetwork_corrected(nn.Module):
  def __init__(self, input_size, layer_sizes):
    super(NeuralNetwork_corrected, self).__init__()

    layers = []
    for i in range(len(layer_sizes) - 1):
      layers.append(nn.Linear(layer_sizes[i], layer_sizes[i+1]))
      layers.append(nn.ReLU())

      # Remove the last ReLU to avoid an activation after the final layer
    layers.pop()

    self.seq = nn.Sequential(*layers)

  def forward(self, x):
    return self.seq(x)