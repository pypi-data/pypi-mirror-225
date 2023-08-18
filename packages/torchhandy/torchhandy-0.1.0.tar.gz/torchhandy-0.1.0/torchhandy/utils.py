import torch
import os
import torch.nn as nn
import math
import time

'''
    This is a wrapped module for swish activation, which is x * sigmoid(x).
    This is not the simplest implement, but perhaps the most similar to other activations.
'''
class Swish(nn.Module):
    def __init__(self):
        self.sig = nn.Sigmoid()
        super().__init__()
    
    def forward(self, x):
        return x * self.sig(x)

def clear_cuda():
    '''
        This function clears out cuda for more spaces. It is extremely useful when you encounter
        an CUDA out-of-memory in the middle of your training process.
    '''
    torch.cuda.empty_cache()
    torch.cuda.empty_cache()
    torch.cuda.empty_cache()
    torch.cuda.empty_cache()
    torch.cuda.empty_cache()
    time.sleep(5)
    torch.cuda.empty_cache()
    torch.cuda.empty_cache()
    torch.cuda.empty_cache()
    torch.cuda.empty_cache()
    torch.cuda.empty_cache()
    
def fea2cha(x):
    '''
        This function accepts an input with shape [bsz, H*H, C] and converts it into
        [bsz, C, H, H]. This often occurs in attentions applied on images.
    '''
    assert(len(x.shape) == 3) # Your input should have exactly 3 dimensions.

    H = int(math.sqrt(x.shape[1]))
    C = x.shape[2]
    y = x.transpose(1, 2).reshape(-1, C, H, H)
    return y

def cha2fea(x):
    '''
        This function accepts an input with shape [bsz, C, H, W] and converts it into
        [bsz, H*W, C]. This often occurs in attentions applied on images.
    '''
    assert(len(x.shape) == 4) # Your input should have exactly 4 dimensions.
    
    C = x.shape[1]
    H = x.shape[2]
    W = x.shape[3]
    
    y = x.transpose(1, 2).transpose(2, 3).reshape(-1, H * W, C)
    return y 

def select_activation(activation):
    '''
        This is a simple function used for selecting activations, note that all the parameters are not tuneable.
        activation : 'relu', 'leakyrelu', 'sigmoid', 'tanh', 'softmax', 'elu', 'gelu', 'swish'
    '''
    act = None
    if activation == 'relu':
        act = nn.ReLU()
    elif activation == 'sigmoid':
        act = nn.Sigmoid()
    elif activation == 'tanh':
        act = nn.Tanh()
    elif activation == 'softmax':
        act = nn.Softmax()
    elif activation == 'elu':
        act = nn.ELU()
    elif activation == 'leakyrelu':
        act = nn.LeakyReLU()
    elif activation == 'gelu':
        act = nn.GELU()
    elif activation == 'swish':
        act = Swish()
        
    return act


def select_normalization(normalization):
    '''
        This is a wrapped function used for selecting normalization method.
        normalization : a tuple, the first element indicates the normalization type:
        0 : layernorm, the second element should be a tuple corresponding to the normalized shape
        1 : 1d-batchnorm, the second element should be the channels to normalize
        2 : 2d-batchnorm, similarly the second element should be the channels to normalize
        -1 : groupnorm, the second element should be the groups and the third element should be the channels to normalize
                to increase robustness, if channels is not divisible by groups, the groups is modified to the greatest common 
                divisers(gcd).
    '''
    norm = None
    try:
        if normalization[0] == 1:
            norm = nn.BatchNorm1d(normalization[1])
        elif normalization[0] == 2:
            norm = nn.BatchNorm2d(normalization[1])
        elif normalization[0] == 0:
            norm = nn.LayerNorm(normalization[1])    
        elif normalization[0] == -1:
            norm = nn.GroupNorm(num_groups = min(normalization[1], math.gcd(normalization[1], normalization[2])),
                                num_channels = normalization[2])
    except Exception as e:
        pass

    return norm

def get_mask(seq_len):
    '''
        Get a typical GPT attention mask.
    '''
    mask0 = torch.full((seq_len, seq_len), -float('inf'))
    mask1 = torch.triu(mask0, diagonal = 1)
    return mask1

def exists(x):
    '''
        Check whether the input is NoneType.
    '''
    return x is not None

def timer_func(func):
    '''
        A basic timing function.
    '''
    def call(*args, **kwargs):
        st = time.time()
        func(*args, **kwargs)
        ed = time.time()
        dur = ed - st
        print(f"time {dur} seconds costed, which is {dur / 60} minutes or {dur / 3600} hours")
    return call