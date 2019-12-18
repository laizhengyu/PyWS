# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 23:45:03 2019

@author: Mr.Lai
"""

import torch
from torch.autograd import Variable

tensor = torch.FloatTensor([[1,2],[3,4]])
variable=Variable(tensor,requires_grad=True) #通过Var计搭建图

t_out = torch.mean(tensor*tensor) #x^2
v_out = torch.mean(variable*variable)


print(t_out)
print(v_out)  #带rrad_fn

v_out.backward()
print(variable.grad)