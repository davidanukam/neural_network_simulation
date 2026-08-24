import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

data_frame: pd.DataFrame = pd.read_csv("package/data/train.csv")

data: np.ndarray = np.array(data_frame)
m, n = data.shape
# m = 42,000, n = 785
# (42000, 785)

# Shuffle the data array
np.random.shuffle(data)

# Make each column = 1 example by transposing the matrix

# data_dev (785, 1000): We are using the first 1000 examples instead of the entire 42,000
data_dev = data[0:1000].T

# Y_dev (1, 1000): Get the first row to get all of the actual labels
# X_dev (784, 1000): Use the rest of the array to later calculate error of weights and biases
Y_dev = data_dev[0]
X_dev = data_dev[1:n] / 255.0

# data_train (785, 41000): For training we want to use the other 41,000 examples
data_train = data[1000:m].T

# Y_train (1, 41000): Get the first row to get all of the actual labels
# X_train (784, 41000): Use the rest of the array to later calculate error of weights and biases
Y_train = data_train[0]
X_train = data_train[1:n] / 255.0


def init_params():
    W1 = np.random.rand(10, 784) - 0.5
    b1 = np.random.rand(10, 1) - 0.5

    W2 = np.random.rand(10, 10) - 0.5
    b2 = np.random.rand(10, 1) - 0.5

    # He/Kaiming initialization scale for ReLU: np.random.randn(...) * np.sqrt(2 / fan_in)
    # W1 = np.random.randn(10, 784) * np.sqrt(2 / 784)
    # b1 = np.zeros((10, 1))

    # W2 = np.random.randn(10, 10) * np.sqrt(2 / 10)
    # b2 = np.zeros((10, 1))

    return W1, b1, W2, b2


def ReLU(Z: np.ndarray):
    return np.maximum(0, Z)


def softmax(Z: np.ndarray):
    # Subtract max per column to prevent exponential explosion
    exp_Z = np.exp(Z - np.max(Z, axis=0, keepdims=True))
    return exp_Z / np.sum(exp_Z, axis=0, keepdims=True)


def forward_prop(
    W1: np.ndarray,
    b1: np.ndarray,
    W2: np.ndarray,
    b2: np.ndarray,
    X: np.ndarray,
):
    A0 = X

    Z1 = W1.dot(A0) + b1
    A1 = ReLU(Z1)

    Z2 = W2.dot(A1) + b2
    A2 = softmax(Z2)

    return Z1, A1, Z2, A2


def one_hot(Y: np.ndarray):
    one_hot_y = np.zeros((Y.size, Y.max() + 1))
    one_hot_y[np.arange(Y.size), Y] = 1
    one_hot_y = one_hot_y.T
    return one_hot_y


def deriv_ReLU(Z: np.ndarray):
    return Z > 0


def back_prop(
    Z1: np.ndarray,
    A1: np.ndarray,
    Z2: np.ndarray,
    A2: np.ndarray,
    W2: np.ndarray,
    X: np.ndarray,
    Y: np.ndarray,
):
    m = Y.size

    one_hot_y = one_hot(Y)

    dZ2 = A2 - one_hot_y
    dW2 = 1 / m * dZ2.dot(A1.T)
    db2 = 1 / m * np.sum(dZ2, 1).reshape(-1, 1)

    dZ1 = W2.T.dot(dZ2) * deriv_ReLU(Z1)
    dW1 = 1 / m * dZ1.dot(X.T)
    db1 = 1 / m * np.sum(dZ1, 1).reshape(-1, 1)

    return dW1, db1, dW2, db2


def update_params(
    W1: np.ndarray,
    b1: np.ndarray,
    W2: np.ndarray,
    b2: np.ndarray,
    dW1: np.ndarray,
    db1: np.ndarray,
    dW2: np.ndarray,
    db2: np.ndarray,
    alpha: float,
):
    W1 -= alpha * dW1
    b1 -= alpha * db1

    W2 -= alpha * dW2
    b2 -= alpha * db2

    return W1, b1, W2, b2


def get_predictions(A2: np.ndarray):
    return np.argmax(A2, 0)


def get_accuracy(predictions, Y: np.ndarray):
    print(predictions, Y)
    return np.sum(predictions == Y) / Y.size


def gradient_descent(
    X: np.ndarray,
    Y: np.ndarray,
    iterations: int,
    alpha: float,
):
    W1, b1, W2, b2 = init_params()

    for i in range(iterations):
        Z1, A1, Z2, A2 = forward_prop(W1, b1, W2, b2, X)
        dW1, db1, dW2, db2 = back_prop(Z1, A1, Z2, A2, W2, X, Y)
        W1, b1, W2, b2 = update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha)

        if i % 50 == 0:
            print("Iteration:", i)
            print("Accuracy:", get_accuracy(get_predictions(A2), Y))

    return W1, b1, W2, b2


# W1, b1, W2, b2 = gradient_descent(X_train, Y_train, 500, 0.1)

# W1, b1, W2, b2 = init_params()


def test(
    W1: np.ndarray,
    b1: np.ndarray,
    W2: np.ndarray,
    b2: np.ndarray,
    X: np.ndarray,
    Y: np.ndarray,
    alpha: float,
):
    Z1, A1, Z2, A2 = forward_prop(W1, b1, W2, b2, X)
    dW1, db1, dW2, db2 = back_prop(Z1, A1, Z2, A2, W2, X, Y)
    W1, b1, W2, b2 = update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha)

    # print("Accuracy:", get_accuracy(get_predictions(A2), Y))

    return W1, b1, W2, b2, get_predictions(A2)


# W1, b1, W2, b2 = init_params()

# for i in range(100):
#     W1, b1, W2, b2 = test(W1, b1, W2, b2, X_train, Y_train, 0.1)
