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

ins = np.array([[0.,0.,0.],
                [0.,0.,1.],
                [0.,1.,0.],
                [0.,1.,1.], 
                [1.,0.,0.],
                [1.,0.,1.],
                [1.,1.,0.],
                [1.,1.,1.]])

expected = np.array([[1.,1],
                     [1.,1],
                     [0.,0],
                     [0.,0],
                     [1.,1],
                     [1.,1],
                     [1.,1],
                     [1.,1]])

pred = np.zeros_like(expected)

# dimensions
ni      = ins.shape[1]
no      = expected.shape[1]
nh      = 8
h_pre    = np.zeros((nh,1), dtype=np.float)
h_post   = np.zeros((nh,1), dtype=np.float)
eta     = 0.25
alpha   = 0.1

#weights
w_ih    = np.random.random((ni,nh))
w_ho    = np.random.random((nh,no))

# previous slope information
c_ih    = np.random.random(w_ih.shape)
c_ho    = np.random.random(w_ho.shape)

#################################################################################
# in -> w_ih -> h_pre -> sigmoid -> h_post -> w_ho -> out_pre -> sigmoid -> out_post
#        |      (err_h_pre)        (err-h_post) |     (err_o_pre)           (err_o_post)
#       c_ih                                   c_oh
#################################################################################

np.set_printoptions(precision=3, suppress=True)
# Training
sse    = 10
epoch = 0
while sse > 0.00001:
    epoch += 1
    sse = 0
    for idx, x in enumerate(ins):
        x        = x.reshape((1,len(x))) # covert from array to matrix # 1 x no
        # -- forward propagation --
        h_pre     = np.dot(x, w_ih)     # 1 x nh
        h_post    = sigmoid(h_pre)       # 1 x nh
        out_pre   = np.dot(h_post, w_ho) # 1 x no
        out_post  = sigmoid(out_pre)     # 1 x no

        # -- error calculation --
        err_o_post    = expected[idx] - out_post   # 1 x no
        err_o_pre   = dsigmoid(out_pre) * err_o_post  # 1 x no
        err_h_post    = np.dot(err_o_pre, w_ho.T)    # 1 x nh
        err_h_pre   = dsigmoid(h_pre) * err_h_post    # 1 x nh (.*)
            
        # -- weights adjustment --
        d_ho     = np.dot(h_post.T, err_o_pre)          # nh x no
        w_ho     = w_ho + eta * d_ho + alpha * c_ho # nh x no
        c_ho     = d_ho.copy() # Store momentum     
        
        d_ih     = np.dot(x.T, err_h_pre)              # ni x nh
        w_ih     = w_ih + eta * d_ih + alpha * c_ih # ni x nh
        c_ih     = d_ih.copy()

        # -- sum of squares error
        sse = sse + np.dot(err_o_post, err_o_post.T)[0,0]
        pred[idx,:] = out_post
    if epoch % 100 == 0:
        print epoch, sse
print "After {0} epochs:".format(epoch)
print pred
