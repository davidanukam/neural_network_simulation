# Neural Network Simulation

Pygame visualization of a neural network while it trains on MNIST.

The window shows the graph on the left (nodes, edges, live weights) and a sidebar on the right with the current prediction, the actual digit, and training accuracy. The trainer is a small fully connected network written in NumPy; a separate PyTorch MNIST classifier lives in the same repo for comparison.

## Features

- Layered graph of nodes and edges (`784 → 10 → 10`)
- Weights drawn inside nodes and updated as training runs
- Output node highlighted for the model's current prediction
- Sidebar: predicted digit, actual digit, and accuracy
- Pan and zoom the graph (mouse-centered zoom)
- One gradient-descent step about once per second

## Architecture

**Visualizer** (`package/sim`): `Network` owns `Layer`s of `Node`s connected by `Edge`s. Camera pan/zoom maps world coordinates to the screen.

**From-scratch trainer** (`package/mnist`): two-layer network (784 → 10 ReLU → 10 softmax), forward pass, backprop, and gradient descent in NumPy. `Simulation` copies averaged weights onto the graph and runs one training step per second.

**PyTorch** (`package/pytorch`): a 784 → 128 → 64 → 10 MLP trained with Adam, plus a short tensor tutorial.

## Requirements

- Python 3.10+
- Windows for the main sim (`pywinstyles` is used for the window title bar)
- MNIST `train.csv` from [Kaggle Digit Recognizer](https://www.kaggle.com/competitions/digit-recognizer/data)

Place the CSV at:

```
package/data/train.csv
```

## Setup

From the repository root:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install pygame pywinstyles numpy pandas matplotlib
```

Optional, for the PyTorch scripts:

```bash
pip install torch torchvision
```

## Run

Always run from the repository root so `package/` imports and `package/data/train.csv` resolve.

**Simulation (NumPy trainer + Pygame):**

```bash
python -m package.sim.main
```

**PyTorch MNIST classifier:**

```bash
python -m package.pytorch.mnist_classifier
```

**Camera pan/zoom sandbox** (no network):

```bash
python -m package.sim.test_camera
```

## Controls

| Input | Action |
| --- | --- |
| Left-drag on the graph | Pan |
| Mouse wheel | Zoom toward the cursor (1×–10×) |
| `R` | Reset pan |
| `0` | Reset zoom to 1× |

## Project layout

```
package/
  sim/          Pygame graph, camera, and main loop
  mnist/        NumPy MNIST trainer (forward, backprop, GD)
  pytorch/      PyTorch classifier and tensor notes
  data/         train.csv (not committed; download from Kaggle)
```
