import torch.nn as nn
import torch
from .utils import select_activation, select_normalization, fea2cha, cha2fea

'''
    This is a typical module in ResNet with 2 conv layers.
'''
class Res_Conv(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, 
                 normalization = None, activation = 'relu'):
        nn.Module.__init__(self)
        self.conv1 = nn.Conv2d(in_channels= in_channels, out_channels= out_channels, 
                            kernel_size= kernel_size, padding= (kernel_size[0] - 1) // 2)
        self.conv2 = nn.Conv2d(in_channels = out_channels, out_channels = out_channels,
                               kernel_size= kernel_size, padding= (kernel_size[0] - 1) // 2)
        self.in_channels = in_channels
        self.out_channels = out_channels

        self.norm = select_normalization(normalization)
        self.act = select_activation(activation)
                
        
    def forward(self, x):
        output = self.conv1(x)
        if self.norm:
            output = self.norm(output)
        if self.act:
            output = self.act(output)
            
        output = self.conv2(output)
        if self.norm:
            output = self.norm(output)
        if self.in_channels == self.out_channels:
            output = output + x
        if self.act:
            output = self.act(output)
        return output
    
'''
    This is a residual convolution layer with one conv.
'''
class SConv(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, 
                 normalization = None, activation = 'relu', res_connection = True):
        nn.Module.__init__(self)
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.res_connection = res_connection
        
        self.conv1 = nn.Conv2d(in_channels= in_channels, out_channels= out_channels, 
                            kernel_size= kernel_size, padding= (kernel_size[0] - 1) // 2)
        self.norm = select_normalization(normalization)
        self.act = select_activation(activation)
                
        
    def forward(self, input):
        output = self.conv1(input)
        if self.norm:
            output = self.norm(output)
        if self.in_channels == self.out_channels and self.res_connection:
            output = output + input
        if self.act:
            output = self.act(output)
        return output
    
'''
    This is a conv module with self-attention layers.
'''
class Att_Conv(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, siz, num_heads, dropout,
                normalization = None, activation = 'relu', res_connection = True):
        nn.Module.__init__(self)
        
        self.conv1 = SConv(in_channels, out_channels, kernel_size, 
                           normalization, activation, res_connection)
        self.conv2 = SConv(out_channels, out_channels, kernel_size, 
                           normalization, activation, res_connection)
        self.norm = nn.LayerNorm((siz * siz, out_channels))
        self.att = nn.MultiheadAttention(out_channels, num_heads, dropout, batch_first = True)
        
    def forward(self, x):
        fea = self.conv1(x)
        a_fea = cha2fea(fea)
        att_out, _ = self.att(a_fea, a_fea, a_fea)
        fea = att_out
        if self.norm:
            fea = self.norm(fea) + a_fea
        fea = fea2cha(fea)
        return self.conv2(fea)