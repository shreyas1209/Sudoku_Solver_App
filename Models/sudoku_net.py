# -*- coding: utf-8 -*-
"""Sudoku_Net.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WTwygQWz50DW6b0aVpws3V9Ka67m2dxa
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import time

class sudokunet(nn.Module):
  def __init__(self,output_classes,in_channels = 1):
    super(sudokunet,self).__init__()
    self.conv1 = nn.Conv2d(1,16,kernel_size = 3,stride = 1,padding = 1) #28x28
    self.pool1 = nn.MaxPool2d(2)
    self.conv2 = nn.Conv2d(16,32,kernel_size = 3, stride = 1,padding = 1) #14x14
    self.pool2 = nn.MaxPool2d(2)
    self.conv3 = nn.Conv2d(32,64,kernel_size = 3, stride = 1,padding = 1) #7x7
    self.output = nn.Linear(7*7*64, output_classes)

  def forward(self,x):
    x = self.conv1(x)
    x = self.pool1(x)
    x = self.conv2(x)
    x = self.pool2(x)
    x = self.conv3(x)
    x = x.reshape(x.shape[0],-1)
    x = self.output(x)
    
    return x



