# This program demonstrates how to stack and take averages of arrays

import numpy as np  # import numpy for handling matrices

a = np.array( [2.1, 3.1] )  # declare a 2x1 vector
print ("a vector:", a)
b = np.array( [2.3, 3.3] ) # declare a second vector
print ("b vector:", b)

# Next we can stack vector a on top of vector b
a_b = np.stack( (a,b) ) # two pairs of parentheses are required
print("a and b stacked:")  # print the output
print(a_b)

# now the "data" array is a 2x2.  the vstack function is required to stack an
# additional array to achieve a 2x3
c = np.array([2.8, 3.8]) # declare one more vector
print("array to add:")
print(c)
a_b_c = np.vstack((a_b,c))
print("final matrix")
print(a_b_c)

data_av = np.average(a_b_c, axis=0)
print("averaged along axis 0 (vertically)")
print(data_av)
