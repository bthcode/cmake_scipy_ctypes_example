#!/usr/bin/env python

import numpy as np
np.set_printoptions(precision=3, suppress=True)

def reverse_enumerate(L):                                                            
    ''' reverse enumerate '''
    for index in reversed(xrange(len(L))):                                       
        yield index, L[index]   
# end reverse_enumerate

def sigmoid(x):
    '''compute sigmoid nonlinearity'''
    output = (2./(1+np.exp(-x))) - 0.5
    return output
# end sigmoid

def dsigmoid(x):
    '''convert output of sigmoid function to its derivative'''
    return 2*np.exp(-x)/(1+np.exp(-x))**2
# end dsigmoid

np.random.seed(1)

# INPUT PREP
data       = open('input.txt', 'r').read() # should be simple plain text file
data       = list(data)
chars      = list(set(data))
data_size  = len(data)
vocab_size = len(chars)
char_to_ix = { ch:i for i,ch in enumerate(chars) } # assigns each char a number - could be done with ord
ix_to_char = { i:ch for i,ch in enumerate(chars) } # reverse lookup

# INITIAL WEIGHTS
num_chars = 8 # take 8 chars at a time
w_ihs     = []
w_hos     = []
w_hhs     = []
hs        = [0] * num_chars

# Each nn has an ih and an ho
eta       = 0.25
alpha     = 0.1
ni        = vocab_size # take one char as input to an individual nn
no        = vocab_size # each layer has one char as output
nh        = 16

# SETUP
for i in range(num_chars):
    w_ihs.append(np.random.random((ni,nh)))
    w_hos.append(np.random.random((nh,no)))
    w_hhs.append(np.random.random((nh,nh)))
# end

print 'data has %d characters, %d unique.' % (data_size, vocab_size)

#################################################################################
# in -> w_ih -> h_in -> sigmoid -> h_out -> w_ho -> out_in -> sigmoid -> out_out
#                                    |
# in -> w_ih -> h_in -> sigmoid -> h_out -> w_ho -> out_in -> sigmoid -> out_out
#                                    |
# in -> w_ih -> h_in -> sigmoid -> h_out -> w_ho -> out_in -> sigmoid -> out_out
#
#################################################################################

# Training
sse      = 10
epoch    = 0
char_idx = 0
set_size = num_chars+1

# Place to put our inputs and outputs
invecs = np.zeros((vocab_size,num_chars))
outvecs = np.zeros((vocab_size,num_chars))
out_in  = np.zeros((vocab_size,num_chars))
out_out = np.zeros((vocab_size,num_chars))
err_os  = np.zeros((vocab_size,num_chars))
err_ops = np.zeros((vocab_size,num_chars))

while sse > 0.00001:
    epoch += 1
    sse = 0

    # ------- Get Current Character Set ------- #
    # grab n+1, handling wrap around
    end_idx = min(len(data), char_idx+set_size)
    ins = data[char_idx:end_idx]
    # wrap around
    if len(ins) < set_size:
        end_idx = set_size - len(ins)
        ins.extend(data[:end_idx])
    char_idx = end_idx
    if char_idx >= len(data):
        char_idx = 0

    # ------- Forward Pass ------- #
    cs = [ char_to_ix[x] for x in ins ]
    for idx, c in enumerate(cs[:-1]):
        invecs[c,idx] = 1
    for idx, c in enumerate(cs[1:]):
        outvecs[c,idx] = 1

    for i in range(num_chars):
        x = invecs[:,i]         # 1 x vocab
        y = outvecs[:,i]        # 1 x vocab
        if i > 0:
            h_in = np.dot(x,w_ihs[i]) + np.dot(hs[i-1], w_hhs[i-1])
        else:
            h_in = np.dot(x,w_ihs[i])
        h_in = np.dot(x, w_ihs[i])    # nh
        h_out = sigmoid(h_in)         # nh
        hs[i] = h_out                 # nh

        out_in[:,i] = np.dot(h_out, w_hos[i]) # no x nchars
        out_out[:,i] = sigmoid(out_in[:,1])                 # no x nchars

    # --------- Error ------------ #
        err_os[:,i]  = outvecs[:,i] - out_out[:,i]              # no x nchars
        err_ops[:,i] = dsigmoid(err_os[:,i]) * err_os[:,i]      # no x nchars (.*)

    for idx, h in reverse_enumerate(hs):
        err_ho[:,i] = np.dot(err_ops[:,i], w_al;ksdjf;laksdjf
        
'''
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
