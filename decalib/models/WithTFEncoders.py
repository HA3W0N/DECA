# -*- coding: utf-8 -*-
#
# Max-Planck-Gesellschaft zur Förderung der Wissenschaften e.V. (MPG) is
# holder of all proprietary rights on this computer program.
# Using this computer program means that you agree to the terms 
# in the LICENSE file included with this software distribution. 
# Any use not explicitly granted by the LICENSE is prohibited.
#
# Copyright©2019 Max-Planck-Gesellschaft zur Förderung
# der Wissenschaften e.V. (MPG). acting on behalf of its Max Planck Institute
# for Intelligent Systems. All rights reserved.
#
# For comments or questions, please email us at deca@tue.mpg.de
# For commercial licensing contact, please contact ps-license@tuebingen.mpg.de

import numpy as np
import torch.nn as nn
import torch
import torch.nn.functional as F
from . import resnet



class ResnetWithTFEncoder(nn.Module):
    def __init__(self, outsize, last_op=None):
        super(ResnetWithTFEncoder, self).__init__()
        feature_size = 2048
        self.encoder = resnet.load_ResNet50Model() #out: 2048
        ### regressor
        self.layers = nn.Sequential(
            nn.Linear(feature_size, 1024),
            nn.ReLU(),
            nn.Linear(1024, outsize)
        )
        ########Including Transformer Encoder########
        # torch.nn.TransformerEncoderLayer(d_model, nhead, dim_feedforward=2048, dropout=0.1, activation=<function relu>,
        # layer_norm_eps=1e-05, batch_first=False, norm_first=False, bias=True, device=None, dtype=None)
        self.transformerencoder1 = nn.TransformerEncoderLayer(d_model=236, nhead=4, dim_feedforward=1024, dropout=0)
        self.transformerencoder2 = nn.TransformerEncoderLayer(d_model=236, nhead=4, dim_feedforward=1024, dropout=0)
        self.transformerencoder3 = nn.TransformerEncoderLayer(d_model=236, nhead=4, dim_feedforward=1024, dropout=0)
        self.last_op = last_op

    def forward(self, inputs):
        features = self.encoder(inputs)
        print("Features: ", features.shape)
        parameters = self.layers(features)
        print("Parameters: ", parameters.shape)
        encode1parameters = self.transformerencoder1(parameters.unsqueeze(0))
        print("Parameters with TFEncoder 1: ", encode1parameters.shape)
        print("Encode parameter1 : ",encode1parameters)
        encode2parameters = self.transformerencoder2(encode1parameters)
        print("Parameters with TFEncoder 2: ", encode2parameters.shape) 
        # print("Encode parameter2 : ",encode2parameters)
        encode3parameters = self.transformerencoder3(encode2parameters).squeeze(0)
        print("Parameters with TFEncoder 3: ", encode3parameters.shape)
        # print("Encode parameter3 : ",encode3parameters)


        if self.last_op:
            parameters = self.last_op(parameters)

        return parameters

