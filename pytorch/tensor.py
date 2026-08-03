import torch

## Creating a tensor ##

# From a list
x = torch.tensor([1.0, 2.0, 3.0])

# Filled with zeros or ones
zeros = torch.zeros(3, 3, 3)
ones = torch.ones(3, 3, 3)

# Random values
rand = torch.rand(2, 3, 4)

# print(x)
# print(zeros)
# print(ones)
# print(rand)

## Basic arithmetic ##
a = torch.tensor([1.0, 2.0, 3.0])
b = torch.tensor([4.0, 5.0, 6.0])

# print(a + b)
# print(a * b)
# print(a.sum())
# print(a.mean())

## Reshaping ##
x = torch.ones(6)
x_reshaped = x.reshape(2, 3)
# print(x_reshaped.shape)

## Moving to GPU ##
if torch.cuda.is_available():
    print("CUDA-enabled GPU is available")
    x = x.to("cuda")

## Converting to and from NumPy ##
import numpy as np

# Tensor to NumPy
tensor = torch.tensor([1.0, 2.0, 3.0])
numpy_array = tensor.numpy()

print("Original PyTorch tensor:")
print(tensor)

print("\nConverted to NumPy array:")
print(numpy_array)

# NumPy to Tensor
numpy_array = np.array([1.0, 2.0, 3.0])
tensor = torch.from_numpy(numpy_array)

print("\nOriginal NumPy array:")
print(numpy_array)

print("\nConverted to PyTorch tensor:")
print(tensor)
