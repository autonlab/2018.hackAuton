#!/usr/biny/env python

"""
plot_train.py
Plot the learning curve.
"""

__version__     = "0.0.1"
__authors__     = [("David Qiu", "dq@cs.cmu.edu"),
                   ("Karthik Paga", "kpaga@andrew.cmu.edu")]
__copyright__   = "Copyright (C) 2018, Hactauton 2018 Dolan Wins Team. All rights reserved."


import os.path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import pdb


def plot_train(fname_train):
  loss_curve = []
  with open(fname_train, 'r') as f:
    while True:
      line = f.readline()
      if line:
        loss_curve.append(float(line))
      else:
        break

  plt.plot([epoch for epoch in range(len(loss_curve))], loss_curve)
  plt.ylabel('loss')
  plt.xlabel('epoch')
  plt.ylim((0, 1))


def main():
  fname_train_value = '../data/value_model_train.log'
  fname_train_behavior = '../data/behavior_model_train.log'

  plt.figure(1)
  plot_train(fname_train_value)
  
  plt.figure(2)
  plot_train(fname_train_behavior)

  plt.show()


if __name__ == '__main__':
  main()

