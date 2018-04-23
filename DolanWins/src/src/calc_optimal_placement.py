#!/usr/biny/env python

"""
calc_optimal_placement.py
Calculate the optimal driver placement.
"""

__version__     = "0.0.1"
__authors__     = [("David Qiu", "dq@cs.cmu.edu"),
                   ("Karthik Paga", "kpaga@andrew.cmu.edu")]
__copyright__   = "Copyright (C) 2018, Hactauton 2018 Dolan Wins Team. All rights reserved."


import os.path
import numpy as np
import cma
import keras
from keras.layers import Dense, Activation
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

import pdb
import pandas as pd


TEST_ENV_INDEX = 0
TEST_VIS_DRV_INDEX = 0
TEST_VIS_DRV_DIM_X = 3 # overspeedtime
TEST_VIS_DRV_DIM_Y = 5 # overspeedmax
TEST_EVAL_INDEX = 9 # total_mpg

model_value = None
model_behavior = None


def calc_optimal_placement(s, a0):
  global model_value
  global model_behavior

  def f(x):
    a = x
    V = model_value.predict(np.array([s]))[0]
    Q = model_behavior.predict(np.array([np.concatenate((s, a))]))[0]
    A = Q - V
    return A[TEST_EVAL_INDEX]

  res = cma.fmin(f, x0=len(a0)*[0], sigma0=0.5)
  a_opt = res[0]

  print('a_opt = %s' % (a_opt))

  return a_opt


def plot_vis_drv(s, a0):
  global model_value
  global model_behavior

  # construct sample points and calculate values
  n_samples = 100
  X = np.linspace(-1.0, 1.0, num=n_samples)
  Y = np.linspace(-1.0, 1.0, num=n_samples)
  Z = np.zeros((n_samples, n_samples))
  flat_X = []
  flat_Y = []
  flat_Z = []
  surf_X = np.zeros((n_samples, n_samples))
  surf_Y = np.zeros((n_samples, n_samples))
  surf_Z = np.zeros((n_samples, n_samples))

  X_S = np.array([s for i in range(n_samples)])
  V = model_value.predict(X_S)

  for i_x in range(n_samples):
    X_SA = []
    for i_y in range(n_samples):
      a = np.array(a0)
      a[TEST_VIS_DRV_DIM_X] = X[i_x]
      a[TEST_VIS_DRV_DIM_Y] = Y[i_y]
      X_SA.append(np.concatenate((s, a)))
    X_SA = np.array(X_SA)
    Q = model_behavior.predict(X_SA)
    A = Q - V
    Z[i_x,:] = A.transpose()[TEST_EVAL_INDEX,:]

  for i_x in range(n_samples):
    for i_y in range(n_samples):
      flat_X.append(X[i_x])
      flat_Y.append(Y[i_y])
      flat_Z.append(Z[i_x, i_y])
      surf_X[i_x, i_y] = X[i_x]
      surf_Y[i_x, i_y] = Y[i_y]
      surf_Z[i_x, i_y] = Z[i_x, i_y]

  # print conditions
  print('s = %s' % (s))
  print('a0 = %s' % (a0))

  # plot the data points
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')
  #ax.scatter(flat_X, flat_Y, flat_Z, c='r', s=1.0, marker='.')
  ax.plot_surface(surf_X, surf_Y, surf_Z, 
    cmap=plt.cm.coolwarm, linewidth=0, antialiased=False)
  ax.set_xlabel('overspeedtime')
  ax.set_ylabel('overspeedmax')
  ax.set_zlabel('total_mpg')
  plt.show()


def main():
  global model_value
  global model_behavior

  fname_model_value = '../data/value_model.json'
  fname_weights_value = '../data/value_model_weights.h5'
  fname_model_behavior = '../data/behavior_model.json'
  fname_weights_behavior = '../data/behavior_model_weights.h5'
  
  fname_info = '../data/info.npy'
  fname_env = '../data/env.npy'
  fname_chart = '../data/chart.npy'
  fname_drv = '../data/drv.npy'

  # load models and weights
  with open(fname_model_value, 'r') as f:
    model_value = keras.models.model_from_json(f.read())
  model_value.load_weights(fname_weights_value)

  with open(fname_model_behavior, 'r') as f:
    model_behavior = keras.models.model_from_json(f.read())
  model_behavior.load_weights(fname_weights_behavior)

  # load data and remove NaNs
  info_raw = np.load(fname_info)
  env_raw = np.load(fname_env)
  chart_raw = np.load(fname_chart)
  drv_raw = np.load(fname_drv)
  info = []
  env = []
  chart = []
  drv = []

  for i in range(len(env_raw)):
    if not (np.isnan(env_raw[i]).any() or np.isnan(chart_raw[i]).any() or np.isnan(drv_raw[i]).any()):
      info.append(info_raw[i])
      env.append(env_raw[i])
      chart.append(chart_raw[i])
      drv.append(drv_raw[i])
  env = np.array(env)
  chart = np.array(chart)
  drv = np.array(drv)

  print('data set loaded (%d/%d)' % (len(info), len(info_raw)))

  # find optimal driver placement
  s = env[TEST_ENV_INDEX]
  a0 = drv[TEST_VIS_DRV_INDEX]

  calc_optimal_placement(s, a0)
  #plot_vis_drv(s, a0)

  print('optimal driver placement calculation finished')


if __name__ == '__main__':
  main()
