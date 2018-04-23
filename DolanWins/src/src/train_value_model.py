#!/usr/biny/env python

"""
train_value_model.py
Train the value model as environmental baseline.
"""

__version__     = "0.0.1"
__authors__     = [("David Qiu", "dq@cs.cmu.edu"),
                   ("Karthik Paga", "kpaga@andrew.cmu.edu")]
__copyright__   = "Copyright (C) 2018, Hactauton 2018 Dolan Wins Team. All rights reserved."


import os.path
import numpy as np
import keras
from keras.layers import Dense, Activation

import pdb
import pandas as pd


model = None


def build_model(input_dim, output_dim, fname_model):
  model = keras.models.Sequential()

  model.add(Dense(32, activation='relu', input_dim=input_dim))
  model.add(Dense(32, activation='relu'))
  model.add(Dense(32, activation='relu'))
  #model.add(Dense(32, activation='relu'))
  model.add(Dense(output_dim, activation='linear'))

  with open(fname_model, 'w') as f:
    f.write(model.to_json())

  optimizer = keras.optimizers.Adam(lr=1e-4, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
  #optimizer = keras.optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=None, decay=0.0)

  model.compile(loss='mean_squared_error', optimizer=optimizer)

  return model


def train_model(trainX, trainY, fname_weights, fname_train, epochs=10, verbose=False):
  global model

  if os.path.isfile(fname_weights):
    model.load_weights(fname_weights)
    pass
  
  hist = model.fit(
    trainX, trainY,
    batch_size=32, epochs=epochs,
    verbose=verbose)

  model.save_weights(fname_weights)

  with open(fname_train, 'a') as f:
    hist_loss = hist.history['loss']
    for i_hist in range(len(hist_loss)):
      f.write('%f\n' % hist_loss[i_hist])

  return hist.history['loss']


def main():
  global model

  env = np.load('../data/env.npy')
  drv = np.load('../data/drv.npy')
  chart = np.load('../data/chart.npy')
  M_env = np.shape(env)[1]
  M_drv = np.shape(drv)[1]
  M_chart = np.shape(chart)[1]

  fname_model = '../data/value_model.json'
  fname_weights = '../data/value_model_weights.h5'
  fname_train = '../data/value_model_train.log'

  input_dim = M_env
  output_dim = M_chart
  model = build_model(input_dim, output_dim, fname_model)

  trainX = []
  trainY = []
  for i in range(len(env)):
    if not (np.isnan(env[i]).any() or np.isnan(drv[i]).any() or np.isnan(chart[i]).any()):
      trainX.append(env[i])
      trainY.append(chart[i])
  trainX = np.array(trainX)
  trainY = np.array(trainY)
  print('processed data set (N=%d/%d)' % (len(trainX),len(env)))

  hist = train_model(
    trainX, trainY,
    fname_weights, fname_train, 
    epochs=100, verbose=True)

  print('training finished')


if __name__ == '__main__':
  main()

