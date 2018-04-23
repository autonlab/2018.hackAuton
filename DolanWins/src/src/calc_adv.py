#!/usr/biny/env python

"""
calc_adv.py
Calculate the driver advantage by subtracting the baseline.
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


def calc_adv(fname_info, fname_env, fname_chart, fname_drv, fname_adv_trip, fname_adv_drv, fname_rank_order):
  global model

  info_raw = np.load(fname_info)
  env_raw = np.load(fname_env)
  chart_raw = np.load(fname_chart)
  drv_raw = np.load(fname_drv)
  info = []
  env = []
  chart = []
  drv = []
  baseline = []
  adv_trip = []
  adv_drv = {}

  # remove NaNs
  for i in range(len(env_raw)):
    if not (np.isnan(env_raw[i]).any() or np.isnan(chart_raw[i]).any() or np.isnan(drv_raw[i]).any()):
      info.append(info_raw[i])
      env.append(env_raw[i])
      chart.append(chart_raw[i])
      drv.append(drv_raw[i])
  env = np.array(env)
  chart = np.array(chart)
  drv = np.array(drv)

  # calculate baseline
  baseline = model.predict(env)

  # calculate and save trip advantages
  adv_trip = chart - baseline
  np.save(fname_adv_trip, adv_trip)

  # cluster driver trip advantages
  adv_drv_dict = {}
  for i in range(len(info)):
    driverId = info[i][2]
    if driverId not in adv_drv_dict:
      adv_drv_dict[driverId] = []
    adv_drv_dict[driverId].append(adv_trip[i][9])

  # calculate the driver advantages
  for driverId in adv_drv_dict:
    meanMpg = np.mean(adv_drv_dict[driverId])
    stdMpg = np.std(adv_drv_dict[driverId])
    adv_drv[driverId] = (meanMpg, stdMpg)

  np.save(fname_adv_drv, adv_drv)

  # rank the drivers
  ori_order = [(driverId, adv_drv[driverId][0], adv_drv[driverId][1]) for driverId in adv_drv]
  ori_order_mpg = [ori_order[i][1] for i in range(len(ori_order))]
  rank_order_idx = list(np.argsort(ori_order_mpg))
  rank_order_idx.reverse()
  rank_order = []

  for i in range(len(rank_order_idx)):
    rank_order.append(ori_order[rank_order_idx[i]])

  np.save(fname_rank_order, rank_order)

  print('rank:')
  for i in range(len(rank_order)):
    print('%s: %f (%f)' % (rank_order[i][0], rank_order[i][1], rank_order[i][2]))


def main():
  global model

  fname_model = '../data/value_model.json'
  fname_weights = '../data/value_model_weights.h5'
  
  fname_info = '../data/info.npy'
  fname_env = '../data/env.npy'
  fname_chart = '../data/chart.npy'
  fname_drv = '../data/drv.npy'
  
  fname_adv_trip = '../data/adv_trip.npy'
  fname_adv_drv = '../data/adv_drv.npy'
  fname_rank_order = '../data/rank_order.npy'

  with open(fname_model, 'r') as f:
    model = keras.models.model_from_json(f.read())
  model.load_weights(fname_weights)

  calc_adv(fname_info, fname_env, fname_chart, fname_drv, fname_adv_trip, fname_adv_drv, fname_rank_order)

  print('advantages calculation finished')


if __name__ == '__main__':
  main()
