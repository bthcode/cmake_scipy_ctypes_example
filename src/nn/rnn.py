#!/usr/bin/env python

import numpy as np

# compute sigmoid nonlinearity
def sigmoid(x):
    output = (2./(1+np.exp(-x))) - 0.5
    return output

# convert output of sigmoid function to its derivative
def dsigmoid(x):
    return 2*np.exp(-x)/(1+np.exp(-x))**2

np.random.seed(1)

# Each nn has an ih and an ho
eta       = 0.25
alpha     = 0.1
ni        = 1 # take one char as input to an individual nn
no        = 1 # each layer has one char as output
nh        = 16

num_chars = 8 # take 8 chars at a time
w_ihs     = []
w_hos     = []
w_hhs     = []

# SETUP
for i in range(num_chars):
    w_ihs.append(np.random.random((ni,nh)))
    w_hos.append(np.random.random((nh,no)))
    w_hhs.append(np.random.random((nh,nh)))
# end

# INPUT PREP
data       = open('input.txt', 'r').read() # should be simple plain text file
chars      = list(set(data))
data_size, vocab_size = len(data), len(chars)
print 'data has %d characters, %d unique.' % (data_size, vocab_size)
char_to_ix = { ch:i for i,ch in enumerate(chars) } # assigns each char a number - could be done with ord
ix_to_char = { i:ch for i,ch in enumerate(chars) } # reverse lookup


import pdb; pdb.set_trace()

'''
#################################################################################
# in -> w_ih -> h_in -> sigmoid -> h_out -> w_ho -> out_in -> sigmoid -> out_out
#        |                                   |
#       c_ih                                c_oh
#################################################################################

np.set_printoptions(precision=3, suppress=True)
# Training
sse    = 10
epoch = 0
while sse > 0.00001:
    epoch += 1
    sse = 0
    for idx, x in enumerate(ins):
        x        = x.reshape((1,len(x))) # covert from array to matrix
        # -- forward propagation --
        h_in     = np.dot(x, w_ih)
        h_out    = sigmoid(h_in)
        out_in   = np.dot(h_out, w_ho)
        out_out  = sigmoid(out_in) 

        # -- error calculation --
        err_o    = expected[idx] - out_out
        err_op   = dsigmoid(out_in) * err_o
        err_h    = np.dot(err_op, w_ho.T)
        err_hp   = dsigmoid(h_in) * err_h
            
        # -- weights adjustment --
        d_ho     = np.dot(h_out.T, err_op)
        w_ho     = w_ho + eta * d_ho + alpha * c_ho
        c_ho     = d_ho.copy() # Store momentum
        
        d_ih     = np.dot(x.T, err_hp)
        w_ih     = w_ih + eta * d_ih + alpha * c_ih
        c_ih     = d_ih.copy()

        # -- sum of squares error
        sse = sse + np.dot(err_o, err_o.T)[0,0]
        pred[idx,:] = out_out
    if epoch % 100 == 0:
        print epoch, sse
print "After {0} epochs:".format(epoch)
print pred
'''
