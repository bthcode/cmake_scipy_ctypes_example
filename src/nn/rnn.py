#!/usr/bin/env python

import numpy as np
import string
np.set_printoptions(precision=3, suppress=True)

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
num_chars = 24 # take 8 chars at a time
w_ihs     = []
w_hos     = []
w_hhs     = []

# Each nn has an ih and an ho
eta       = 0.1
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
# in -> w_ih -> h_pre -> sigmoid -> h_post -> w_ho -> out_pre -> sigmoid -> out_post
#                                    |
#                                  w_hh
#                                    |
# in -> w_ih -> h_pre -> sigmoid -> h_post -> w_ho -> out_pre -> sigmoid -> out_post
#                                    |
#                                   w_hh
#                                    |
# in -> w_ih -> h_pre -> sigmoid -> h_post -> w_ho -> out_pre -> sigmoid -> out_post
#
#################################################################################

# Training
sse      = 10
epoch    = 0
char_idx = 0
set_size = num_chars+1

# Place to put our inputs and outputs
invecs     = [ np.zeros((1,vocab_size)) for i in range(num_chars) ]
outvecs    = [ np.zeros((1,vocab_size)) for i in range(num_chars) ]
h_pre      = [ np.zeros((1,nh)) for i in range(num_chars) ]
h_post     = [ np.zeros((1,nh)) for i in range(num_chars) ]
out_pre    = [ np.zeros((1,vocab_size)) for i in range(num_chars) ]
out_post   = [ np.zeros((1,vocab_size)) for i in range(num_chars) ]
err_o_post = [ np.zeros((1,vocab_size)) for i in range(num_chars) ]
err_o_pre  = [ np.zeros((1,vocab_size)) for i in range(num_chars) ]
err_h_post = [ np.zeros((1,nh)) for i in range(num_chars) ]
err_h_pre  = [ np.zeros((1,nh)) for i in range(num_chars) ]

#sample_ix = sample(h_post[0], cs[0], 500, w_ihs[0], w_hhs[0], w_hos[0], vocab_size)
def sample(h, seed_ix, n, Wxh, Whh, Why, vocab_size):
  """ 
  sample a sequence of integers from the model 
  h is memory state, seed_ix is seed letter for first time step
  """
  x = np.zeros((1,vocab_size))
  x[0,seed_ix] = 1
  ixes = []
  for t in xrange(n):
    #h_pre[i] = np.dot(x,w_ihs[i]) + np.dot(h_post[i-1], w_hhs[i-1])
    #print x.shape
    #print Wxh.shape
    #print h.shape
    #print Whh.shape
    h = np.tanh(np.dot(x, Wxh) + np.dot(h,Whh))
    #out_pre[i] = np.dot(h_post[i], w_hos[i]) # no x nchars
    y = np.dot(h,Why)
    p = np.exp(y) / np.sum(np.exp(y))
    ix = np.random.choice(range(vocab_size), p=p.ravel())
    x = np.zeros((1,vocab_size))
    x[0,ix] = 1
    ixes.append(ix)
  return ixes
# end sample


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
        invecs[idx].fill(0)
        invecs[idx][0,c] = 1
    for idx, c in enumerate(cs[1:]):
        outvecs[idx].fill(0)
        outvecs[idx][0,c] = 1

    for i in range(num_chars):
        x = invecs[i]         # 1 x vocab
        y = outvecs[i]        # 1 x vocab
        if i > 0:
            h_pre[i] = np.dot(x,w_ihs[0]) + np.dot(h_post[i-1], w_hhs[0])
        else:
            h_pre[i] = np.dot(x,w_ihs[0])
        h_post[i] = sigmoid(h_pre[i])         # nh

        out_pre[i] = np.dot(h_post[i], w_hos[0]) # no x nchars
        out_post[i] = sigmoid(out_pre[i])                 # no x nchars

    # --------- Error ------------ #
    for i in range(num_chars):
        err_o_post[i]  = outvecs[i] - out_post[i]              # no 
        err_o_pre[i] = dsigmoid(out_pre[i]) * err_o_post[i]      # no (.*)

    for i in range(num_chars):
        idx = num_chars - i - 1 # reverse iterator
        if i == 0: # no net to the right
            err_h_post[idx] = np.dot(err_o_pre[i], w_hos[0].T) # nh
        else:      # net to the right
            #layer_1_delta = (future_layer_1_delta.dot(synapse_h.T) + layer_2_delta.dot(synapse_1.T)) * sigmoid_output_to_derivative(layer_1)
            err_h_post[idx] = np.dot(err_o_pre[i], w_hos[0].T) + np.dot(err_h_pre[idx+1], w_hhs[0]) # nh
        err_h_pre[idx] = dsigmoid(err_h_post[idx]) * err_h_post[idx] #nh (.*)

        
    # --------- Update ---------- #
    for i in range(num_chars):
        d_ho     = np.dot(h_post[i].T, err_o_pre[i])
        w_hos[0] = w_hos[0] + eta * d_ho 
        d_ih     = np.dot(invecs[i].T, err_h_pre[i])
        w_ihs[0] = w_ihs[0] + eta * d_ih 

    # --------- SSE -------------- #
    sse = 0
    for i in range(num_chars):
        sse = sse + np.dot(err_o_post[i], err_o_post[i].T)[0,0]
    sse = sse / float(num_chars)

    if epoch % 1000 == 0:
        #def sample(h, seed_ix, n, Wxh, Whh, Why, vocab_size):
        print "________{0}_________".format(sse)
        sample_ix = sample(h_post[0], cs[0], 500, w_ihs[0], w_hhs[0], w_hos[0], vocab_size)
        sample_ix = [ ix_to_char[ix] for ix in sample_ix ]
        print string.join(sample_ix, '')
'''
        x        = x.reshape((1,len(x))) # covert from array to matrix
        # -- forward propagation --
        h_in     = np.dot(x, w_ih)
        h_out    = sigmoid(h_in)
        out_pre   = np.dot(h_out, w_ho)
        out_post  = sigmoid(out_pre) 


        # -- error calculation --
        err_o    = expected[idx] - out_post
        err_op   = dsigmoid(out_pre) * err_o
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
        pred[idx,:] = out_post
    if epoch % 100 == 0:
        print epoch, sse
print "After {0} epochs:".format(epoch)
print pred
'''
