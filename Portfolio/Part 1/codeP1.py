import random, sys, copy
import numpy as np
import matplotlib as plt

stopValue = 0.05    # What difference the values need to be before the algorithm stops

nodes = [4, 4, 1]

# Weights for the connections between the nodes
## Input -> hidden layer
W1 = np.random.rand(nodes[0], nodes[1])
## Hidden layer -> output
W2 = np.random.rand(nodes[1], nodes[2])

dW1 = np.zeros((nodes[0], nodes[1]))
dW2 = np.zeros((nodes[1], nodes[2]))

#
# Util functions
#
def sigFunc(n):
    """
    Sigmoid function
    """
    return 1 / (1 + np.exp(-n))

def sigPrimeFunc(n):
    """
    The derivative of the sigFunc
    """
    return np.exp(-n)/((1+np.exp(-n))**2)

def isEven(i: int) -> int:
    """
    Is number even or odd

    Return: 
        - 0 if even
        - 1 if odd
    """
    return i % 2

def normalizeData(x, bits):
    """
    Normalize the data from 0 to 1    
    """
    return (x - 0) / (2**bits - 0)

def intToSplitBites(i: int, numLen: int) -> list[list]:
    """
    Split a int into 4 bite chunks, to it can be used as a input to the model
    """
    # Set up things
    b = format(i, 'b')
    arr = np.zeros(numLen)

    bLen = len(b) - 1
    numLen = numLen - 1

    # Fill arr with number from b. Adding from the back
    for i in range(len(b)):
        arr[numLen - i] = b[bLen - i]

    arr = np.array_split(arr, 4)

    # convert every chunk to a number, so there is a 4X1 array of items
    outArr = np.zeros(4)

    for i in range(len(arr)):
        part = arr[i]
        n = part.dot(2**np.arange(part.size)[::-1])    
        outArr[i] = n

    # outArr = np.append(0, outArr)

    return np.array([outArr]).T

#
# ANN code
#
def train():
    pass

def forwardPropagate(x):
    """
    Forward propagate the network
    """
    global W1, W2

    # Compute Feed forward for input to hidden layer 1
    w0 = np.dot(W1, x)
    w0 = sigFunc(w0)

    # Compute Feed forward for hidden layer 1 to output
    w1 = np.dot(W2.T, w0)
    w1 = sigFunc(w1)

    return w0, w1

def calcError(w0, w1, y):
    """
    Calculate the error matrix's
    """
    global W1, W2

    # Error matrix form the hidden layer to output
    err2 = (w1 - y) * (w1) * (1 - w1)
    eW1 = np.dot(W2, err2)
    out2 = 1 - w1
    eW1 = np.multiply(eW1, out2)

    # Error matrix from the hidden layer to hidden layer
    err1 = (w0 - w1) * (w0) * (1 - w0)
    eW0 = np.dot(W1, err1)
    out1 = 1 - w0
    eW0 = np.multiply(eW0, out1)

    return eW0, eW1, err1, err2
    

def backwardsPropagate(x, y, eW0, eW1, err1, err2, learnRate: float):
    """
    Backwards propagate the network
    """
    global W1, W2
    # The gradient vector (gv) for hidden layer to output
    gvW2 = np.true_divide(W2, eW1)
    W2 = W2 - learnRate * gvW2
    
    gvW1 = np.true_divide(W1, eW0)
    W2 = W2 - learnRate * gvW1
    

def runPreception(learningRate) -> int:
    """
    Run the preceptron algorithm.

    Returns: the amount of epochs the algorithm have used
    """
    global W1, W2

    bits = 4
    r = 1000

    for e in range(r + 1):
        # print(f'W1: {W1}')
        # print(f'W2: {W2}')

        num = random.randint(1, 2**bits)

        y = isEven(num)
        y = np.array([[y]])

        x = intToSplitBites(num, bits)
        x = normalizeData(x, bits)
        # x = np.append(x, 0)
        # x = np.array([x]).T

        w0, w1 = forwardPropagate(x)

        # Calculate error
        eW0, eW1, err1, err2 = calcError(w0, w1, y)

        backwardsPropagate(x, y, eW0, eW1, err1, err2, learningRate)

        # progress = (e-0)/((r-1)-0) * 100
        # sys.stdout.write(f'\rProgress: {round(progress,1)}%')
        # sys.stdout.flush()
    else:
        print()
        return e

if __name__ == '__main__':
    epoch = runPreception(0.05)

    testInt = 14

    x = intToSplitBites(testInt, 4)
    x = normalizeData(x, 4)
    w1, w2 = forwardPropagate(x)
    print(w2)

    testInt = 13

    x = intToSplitBites(testInt, 4)
    x = normalizeData(x, 4)
    w1, w2 = forwardPropagate(x)
    print(w2)