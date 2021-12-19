from os import access
import random, sys, copy
from matplotlib.pyplot import axis
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

def normalizeData(i, bits):
    """
    Normalize the data from 0 to 1    
    """
    return (i - 0) / (2**bits - 0)

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

def forwardPropagate(i):
    """
    Forward propagate the network.
    Calculating using matrix's 

    Return:
        - Output of hidden layer
        - Output
    """
    global W1, W2

    # Calculate Feed forward for input to hidden layer 1
    net_h = np.dot(W1, i)   # Net H
    oh = sigFunc(net_h)     # Out H

    # Calculate Feed forward for hidden layer 1 to output
    net_o = np.dot(W2.T, oh)    # Net out 
    o = sigFunc(net_o)          # Out 

    oDer = o * (1 - o)

    return oh, o, oDer

def calcFPError(y, o):
    """
    Calculate the error matrix
    """
    # NOTE: Maybe not add a - to this?
    oErr = (o - y)

    # Calculate the derivative activation function
    do = np.multiply(o, 1 - o)

    return np.multiply(oErr, do)

def calcError(errMat, o, i):
    """
    Calculate the error matrix's
    """
    global W1, W2

    oDer = o * (1 - o)

    # Error matrix form the hidden layer to output
    eW1 = np.matmul(W2, errMat)     # weight matrix X error matrix
    em2 = np.multiply(eW1, oDer)    # prev * (Hadamard) derivative of activation function -> Error matrix 2

    # Error matrix from the hidden layer to hidden layer
    eW0 = np.matmul(W1, em2)    # weight matrix X error matrix 2
    em1 = np.multiply(eW0, i)   # prev * (Hadamard) input nodes

    return em1, em2

def calcQuadraticCost(y, o):
    """
    Calculate the quadratic cost of the current training sett
    """
    return np.power(y - o,2) / 2
    
def backwardsPropagate(oh, em1, em2, i, learningRate):
    """
    Backwards propagate the network
    """
    global W1, W2

    # a = error matrix delta | Rar s = delta feil

    # Partial Derivative C 2
    # pdC2 = np.multiply(oh, errMat)
    
    # Set new values for the weight (hidden layer -> output)
    W2 = W2 - learningRate * np.multiply(oh, em2)

    # Partial Derivative C1
    # pdC1 = np.multiply(i, )

    # Set new values for the weight (input -> hidden layer)
    W1 = W1 - learningRate * np.multiply(em1, i)


    """
    # The gradient vector (gv) for hidden layer to output
    gvW2 = np.true_divide(W2, eW1)
    W2 = W2 - learnRate * gvW2
    
    gvW1 = np.true_divide(W1, eW0)
    W2 = W2 - learnRate * gvW1
    """

    #return pdC1, pdC2

def testFunc():
    rNum = random.randint(1, 2**bits)
    i = np.array(
        normalizeData(
            intToSplitBites(
                rNum,
                bits
            ),
            bits
        ).T
    )

    y = np.array([[isEven(rNum)]])

    for _ in range(0):
        num = random.randint(1, 2**bits)

        ty = isEven(num)
        ty = np.array([[ty]])
        y = np.append(y, ty, axis=0)

        ti = intToSplitBites(num, bits)
        ti = normalizeData(ti, bits)
        ti = np.array(ti.T)
        i = np.append(i, ti, axis=0)

    return i, y

def runPreception(bits, learningRate) -> int:
    """
    Run the preceptron algorithm.

    Returns: the amount of epochs the algorithm have used
    """
    global W1, W2

    showProgress = True
    r = 1000000

    for e in range(r + 1):

        num = random.randint(1, 2**bits)

        y = isEven(num)
        y = np.array([[y]])

        i = intToSplitBites(num, bits)
        i = normalizeData(i, bits)

        # Get out hidden layer and output from the forward propagate
        oh, o, oDer = forwardPropagate(i)

        # Calculate error
        ## Get error matrix
        errMat = calcFPError(y, o)

        ## Get error matrix 1 and error matrix 2
        em1, em2 = calcError(errMat, o, i)
        
        # print(num, o, errMat)

        backwardsPropagate(oh, em1, em2, i, learningRate)

        if showProgress:
            progress = (e-0)/((r-1)-0) * 100
            sys.stdout.write(f'\rProgress: {round(progress,1)}%')
            sys.stdout.flush()
    else:
        if showProgress:
            print()
        return e

if __name__ == '__main__':
    bits = 4

    epoch = runPreception(bits, 0.5)

    print()
    testInts = [14, 15]

    for ti in testInts:
        i = intToSplitBites(ti, bits)
        i = normalizeData(i, bits)
        oh, o, oDer = forwardPropagate(i)
        print(ti, o)

"""
# Notes
a: matrix of activation for each node
z: matrix input values to each node
W: weights
X: Input values
Y: target value
"""