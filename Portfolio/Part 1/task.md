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

# Sources
- https://medium.com/@tiago.tmleite/neural-networks-multilayer-perceptron-and-the-backpropagation-algorithm-a5cd5b904fde
- https://www.cse.unsw.edu.au/~cs9417ml/MLP2/BackPropagation.html

- https://www.delftstack.com/howto/python/python-int-to-binary/
- https://machinelearningmastery.com/implement-backpropagation-algorithm-scratch-python/
- https://towardsdatascience.com/implementing-backpropagation-with-style-in-python-da4c2f49adb4
- https://www.stackvidhya.com/how-to-normalize-data-between-0-and-1-range/
- https://en.wikipedia.org/wiki/Hadamard_product_(matrices)

## Numpy things
- https://stackoverflow.com/questions/5954603/transposing-a-1d-numpy-array
- https://stackoverflow.com/questions/41069825/convert-binary-01-numpy-to-integer-or-binary-string
- https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
- https://numpy.org/doc/stable/reference/generated/numpy.append.html
- https://stackoverflow.com/questions/40034993/how-to-get-element-wise-matrix-multiplication-hadamard-product-in-numpy
- https://numpy.org/doc/stable/reference/generated/numpy.divide.html
- https://numpy.org/doc/stable/reference/generated/numpy.matmul.html
- https://pynative.com/python-range-for-float-numbers/

# Presentations from leachers
- https://hiof.instructure.com/courses/5088/files/folder/Lecture%20Slides/Week%206_Artificial%20Neural%20Network?preview=990559
- https://hiof.instructure.com/courses/5088/files/folder/Lecture%20Slides/Week%206_Artificial%20Neural%20Network?preview=992754
- https://hiof.instructure.com/courses/5088/files/folder/Lecture%20Slides/Week%206_Artificial%20Neural%20Network?preview=988454
- https://hiof.instructure.com/courses/5088/files/folder/Lecture%20Slides/Week%206_Artificial%20Neural%20Network?preview=990569
- https://hiof.instructure.com/courses/5088/files/folder/Lecture%20Slides/Week%206_Artificial%20Neural%20Network?preview=990568

# Videos:
## Youtube chanel: Welch Labs (https://www.youtube.com/channel/UConVfxXodg78Tzh5nNu85Ew)
### Playlist used:
- https://www.youtube.com/watch?v=bxe2T-V8XRs&list=PLiaHhY2iBX9hdHaRr6b7XevZtgZRa1PoU

## Other videos:
- https://www.youtube.com/watch?v=aircAruvnKk
- https://www.youtube.com/watch?v=QJoa0JYaX1I
- https://www.youtube.com/watch?v=Ilg3gGewQ5U