# Part 1 Task
Implement a two-layer perceptron with backpropagation algorithm to solve the parity problem. The desired output for the parity problem is 1 if an input pattern contains an odd number of 1's; otherwise, the output is 0.

Use a network with:
- 4 binary input elements 
- 4 hidden units for the first layer
- 1 output unit for the second layer. 
- Stops when an absolute (difference) of 0.05 is reached for every input pattern.

Other implementation details are:
* Initialize all weights and biases to random numbers between -1 and 1.
* Use a logistic sigmoid with a = 1 as the activation function for all units.

After programming is done, vary the value of learning rate from 0.05 to 0.5 with increment 0.05, and report the number of epochs for each choice of learning rate.
You should use proper graph to analyze the implementation and the relationship between the learning rate and the the number of epochs.