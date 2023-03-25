# стахастический градиентный спуск
# https://www.youtube.com/watch?v=bXGBeRzM87g&list=PLOSf9rRg-fvJt5adxPbefB394QBtW9smZ&index=5

from multiprocessing import Barrier
import random
import numpy as np
from sklearn import datasets


INPUT_DIM = 4
OUT_DIM = 5
H_DIM = 10

def relu(t):
    # return np.maximum(0, t)
    return t

def softmax(t):
    out = np.exp(t)
    return out / np.sum(out)

def softmax_batch(t):
    out = np.exp(t)
    # print(out / np.sum(out, axis=1, keepdims=True))
    return out / np.sum(out, axis=1, keepdims=True)

def sparse_cross_entropy(z, y):
    return -np.log(z[0, y])

def sparse_cross_entropy_batch(z, y):
    return -np.log(np.array([z[j, y[j]] for j in range(len(y))]))

def to_full(y, num_classes):
    y_full = np.zeros((1, num_classes))
    # print(y_full)
    y_full[0, y] = 1
    return y_full

def to_full_batch(y, num_classes):
    y_full = np.zeros((len(y), num_classes))
    for j, yj in enumerate(y):
        y_full[j, yj] = 1
    return y_full

def relu_deriv(t):
    return (t >= 0).astype(float)

iris = datasets.load_iris()
dataset = [(iris.data[i][None, ...], iris.target[i]) for i in range(len(iris.target))]

# x = np.random.randn(1, INPUT_DIM)
# y = random.randint(0, OUT_DIM - 1)

# для угадывания изначально выставляем рандом
W1 = np.random.randn(INPUT_DIM, H_DIM)
b1 = np.random.randn(1, H_DIM)
W2 = np.random.randn(H_DIM, OUT_DIM)
b2 = np.random.randn(1, OUT_DIM)

# W1 = np.array([[ 0.33462099,  0.10068401,  0.20557238, -0.19043767,  0.40249301, -0.00925352,  0.00628916,  0.74784975,  0.25069956, -0.09290041 ],
#                [ 0.41689589,  0.93211640, -0.32300143, -0.13845456,  0.58598293, -0.29140373, -0.28473491,  0.48021000, -0.32318306, -0.34146461 ],
#                [-0.21927019, -0.76135162, -0.11721704,  0.92123373,  0.19501658,  0.00904006,  1.03040632, -0.66867859, -0.01571104, -0.08372566 ],
#                [-0.67791724,  0.07044558, -0.40981071,  0.62098450, -0.33009159, -0.47352435,  0.09687051, -0.68724299,  0.43823402, -0.26574543 ]])

# b1 =  np.array([-0.34133575, -0.24401602, -0.06262318, -0.30410971, -0.37097632,  0.02670964, -0.51851308,  0.54665141,  0.20777536, -0.29905165 ])

# W2 = np.array([[ 0.41186367,  0.15406952, -0.47391773 ],
#                [ 0.79701137, -0.64672799, -0.06339983 ],
#                [-0.20137522, -0.07088810,  0.00212071 ],
#                [-0.58743081, -0.17363843,  0.93769169 ],
#                [ 0.33262125,  0.18999841, -0.14977653 ],
#                [ 0.04450406,  0.26168097,  0.10104333 ],
#                [-0.74384144,  0.33092591,  0.65464737 ],
#                [ 0.45764631,  0.48877246, -1.16928700 ],
#                [-0.16020630, -0.12369116,  0.14171301 ],
#                [ 0.26099978,  0.12834471,  0.20866959 ]])

# b2 =  np.array([-0.16286677,  0.06680119, -0.03563594 ])

ALPHA = 0.00001               # скорость обучения
NUM_EPOCHS = 4000
BATCH_SIZE = 10

loss_arr = []

for ep in range(NUM_EPOCHS):
    random.shuffle(dataset)
    # for i in range(len(dataset) // BATCH_SIZE):
    for i in range(len(dataset)):

        # batch_x, batch_y = zip(*dataset[i * BATCH_SIZE: i * BATCH_SIZE + BATCH_SIZE])
        # x = np.concatenate(batch_x, axis=0)
        # y = np.array(batch_y)

        x, y = dataset[i]

        # # Forward 
        t1 = x @ W1 + b1
        h1 = relu(t1)
        t2 = h1 @ W2 + b2
        z = softmax(t2)
        E = sparse_cross_entropy(z, y)
        
        # z = softmax_batch(t2)
        # E = np.sum(sparse_cross_entropy_batch(z, y))

        # # Backward
        y_full = to_full(y, OUT_DIM)
        # y_full = to_full_batch(y, OUT_DIM)
        dE_dt2 = z - y_full
        dE_dW2 = h1.T @ dE_dt2
        dE_db2 = dE_dt2
        # dE_db2 = np.sum(dE_dt2, axis=0, keepdims=True)
        dE_dh1 = dE_dt2 @ W2.T
        dE_dt1 = dE_dh1 * relu_deriv(t1)
        dE_dW1 = x.T @ dE_dt1
        dE_db1 = dE_dt1
        # dE_db1 = np.sum(dE_dt1, axis=0, keepdims=True)

        # # Update
        W1 = W1 - ALPHA * dE_dW1
        b1 = b1 - ALPHA * dE_db1
        W2 = W2 - ALPHA * dE_dW2
        b2 = b2 - ALPHA * dE_db2

        loss_arr.append(E)

def predict(x):                     # определение значения
    t1 = x @ W1 + b1                # @ - перемножение двух матриц
    h1 = relu(t1)
    t2 = h1 @ W2 + b2
    z = softmax(t2)
    return z

def calc_accuracy():
    correct = 0
    for x, y in dataset:
        z = predict(x)
        y_pred = np.argmax(z)
        if y_pred == y:
            correct += 1
    acc = correct / len(dataset)
    return acc

accuracy = calc_accuracy()
print("Accuracy:", accuracy)

import matplotlib.pyplot as plt
plt.plot(loss_arr)
plt.show()

print(W1)
print(b1)
print(W2)
print(b2)