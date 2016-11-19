#!/usr/bin/env python

import numpy as np
import string
np.set_printoptions(precision=3, suppress=True)

np.random.seed(1)

class rnn:
    def __init__(self, vocab_size, num_chars):
        self.vocab_size = vocab_size

        self.num_chars = num_chars

        # Each nn has an ih and an ho
        self.eta   = 0.1
        self.ni    = self.vocab_size # take one char as input to an individual nn
        self.no    = self.vocab_size # each layer has one char as output
        self.nh    = 100

        self.w_ih  = np.random.randn(self.nh,self.ni)*0.01
        self.w_hh  = np.random.randn(self.nh,self.nh)*0.01
        self.w_ho  = np.random.randn(self.no,self.nh)*0.01

        self.bh    = np.zeros((self.nh, 1)) # hidden bias
        self.by    = np.zeros((self.ni, 1)) # output bias

        self.m_w_ih  = np.zeros_like(self.w_ih)
        self.m_w_hh  = np.zeros_like(self.w_hh)
        self.m_w_ho  = np.zeros_like(self.w_ho)

        self.m_bh   = np.zeros_like(self.bh)
        self.m_by   = np.zeros_like(self.by)

        self.hprev = np.zeros((self.nh,1))
        self.smooth_loss = -np.log(1.0/self.vocab_size)*self.num_chars
    # end __init__       

    def train(self, chars):
        # ------- Forward Pass ------- #
        inputs  = chars[:-1]
        targets = chars[1:]

        loss = 0

        hs = {}
        xs = {}
        ys = {}
        ps = {}

        hs[-1] = np.copy(self.hprev)

        ## Forward Pass ##
        for t in xrange(len(inputs)):
            char_index = inputs[t]
            out_index  = targets[t]
            xs[t] = np.zeros((vocab_size,1))
            xs[t][char_index] = 1
            hs[t] = np.tanh(np.dot(self.w_ih,xs[t]) + np.dot(self.w_hh,hs[t-1])+self.bh) # hidden state
            ys[t] = np.dot(self.w_ho, hs[t]) + self.by  # unnormalized log probabilities for next chars
            ps[t] = np.exp(ys[t]) / np.sum(np.exp(ys[t])) # probabilities for next chars
            prob  = ps[t][out_index,0]
            loss += -np.log(prob) # softmax (cross-entropy loss)

        ## Back Propagation ##

        d_w_ih = np.zeros_like(self.w_ih)
        d_w_hh = np.zeros_like(self.w_hh)
        d_w_ho = np.zeros_like(self.w_ho)

        d_bh = np.zeros_like(self.bh)
        d_by = np.zeros_like(self.by)
        d_hnext = np.zeros_like(hs[0])

        for t in reversed(xrange(len(inputs))):
            dy = np.copy(ps[t])
            dy[targets[t]] -= 1 # backprop into y. see http://cs231n.github.io/neural-networks-case-study/#grad if confused here
            d_w_ho += np.dot(dy, hs[t].T)
            d_by += dy
            d_h = np.dot(self.w_ho.T, dy) + d_hnext # backprop into h
            d_hraw = (1 - hs[t] * hs[t]) * d_h # backprop through tanh nonlinearity
            d_bh += d_hraw
            d_w_ih += np.dot(d_hraw, xs[t].T)
            d_w_hh += np.dot(d_hraw, hs[t-1].T)
            d_hnext = np.dot(self.w_hh.T, d_hraw)
        for dparam in [d_w_ih, d_w_hh, d_w_ho, d_bh, d_by]:
            np.clip(dparam, -5, 5, out=dparam) # clip to mitigate exploding gradients

        self.hprev = hs[len(inputs)-1]

        self.m_w_ih = self.m_w_ih + d_w_ih * d_w_ih
        self.w_ih   = self.w_ih - self.eta * d_w_ih / np.sqrt(self.m_w_ih + 1e-8)
        self.m_w_hh = self.m_w_hh + d_w_hh * d_w_hh
        self.w_hh   = self.w_hh - self.eta * d_w_hh / np.sqrt(self.m_w_hh + 1e-8)
        self.m_w_ho = self.m_w_ho + d_w_ho * d_w_ho
        self.w_ho   = self.w_ho - self.eta * d_w_ho / np.sqrt(self.m_w_ho + 1e-8)

        self.m_bh   = self.m_bh + d_bh * d_bh
        self.bh     = self.bh   - self.eta * d_bh / np.sqrt(self.m_bh + 1e-8)
        self.m_by   = self.m_by + d_by * d_by
        self.by     = self.by   - self.eta * d_by / np.sqrt(self.m_by + 1e-8)

        return loss
    # end train

    def sample(self, nchars, seed_ix):
        """ 
        sample a sequence of integers from the model 
        h is memory state, seed_ix is seed letter for first time step
        """
        x = np.zeros((self.vocab_size,1))
        x[seed_ix] = 1
        ixes = []
        h = self.hprev.copy()
        for t in range(nchars):
            h = np.tanh(np.dot(self.w_ih,x) + np.dot(self.w_hh,h)) # hidden state
            y = np.dot(self.w_ho, h)
            p = np.exp(y) / np.sum(np.exp(y))
            ix = np.random.choice(range(self.vocab_size), p=p.ravel())
            x = np.zeros((self.vocab_size,1))
            x[ix] = 1
            ixes.append(ix)
        return ixes
    # end sample


# end class rnn

if __name__=="__main__":
    # INPUT PREP
    data       = open('input.txt', 'r').read() # should be simple plain text file
    data       = list(data)
    chars      = list(set(data))
    data_size  = len(data)
    vocab_size = len(chars)
    char_to_ix = { ch:i for i,ch in enumerate(chars) } # assigns each char a number - could be done with ord
    ix_to_char = { i:ch for i,ch in enumerate(chars) } # reverse lookup
    num_chars  = 25

    R          = rnn(vocab_size, num_chars)

    # Training
    epoch    = 0
    char_idx = 0
    set_size = num_chars+1

    loss = 10000
    smooth_loss = -np.log(1.0/vocab_size)*num_chars
    while loss > 0.00001:
        epoch += 1
        loss = 0

        # ------- Get Current Character Set ------- #
        # grab n+1, handling wrap around
        end_idx = min(len(data), char_idx+set_size)
        ins = data[char_idx:end_idx]

        # wrap around
        if len(ins) < set_size:
            end_idx = set_size - len(ins)
            ins.extend(data[:end_idx])
        char_idx = end_idx-1
        if char_idx >= len(data):
            char_idx = 0
            R.hprev = np.zeros((R.nh,1)) # reset RNN memory

        cs = [ char_to_ix[x] for x in ins ]
        loss = R.train(cs)
        smooth_loss = smooth_loss * 0.999 + loss * 0.001

        if epoch % 100 == 0:
            print "-------------- Epoch : {0}, loss = {1} ".format(epoch, smooth_loss)
        if epoch % 1000 == 0:
            print ins
            sample_idxs = R.sample(500, cs[0])
            sample_chars = [ ix_to_char[ix] for ix in sample_idxs ]
            print string.join(sample_chars, '')
