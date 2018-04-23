#!/usr/biny/env python

"""
preproc_data.py
Preprocess the data.
"""

__version__     = "0.0.1"
__authors__     = [("David Qiu", "dq@cs.cmu.edu"),
                   ("Karthik Paga", "kpaga@andrew.cmu.edu")]
__copyright__   = "Copyright (C) 2018, Hactauton 2018 Dolan Wins Team. All rights reserved."


import numpy as np

import pdb
import pandas as pd


def proc_data(fname_in, fname_out_info, fname_out_env, fname_out_drv, fname_out_chart):
  """
  Process the data.

  @param fname_in The input file name.
  @param fname_out_info The info data file name.
  @param fname_out_env The environment data file name.
  @param fname_out_drv The driver data file name.
  @param fname_out_char The trip characteristic data file name.
  @return N The number of items processed.
  @return M_info The number of dimensions of the info data.
  @return M_env The number of dimensions of the env data.
  @return M_drv The number of dimensions of the drv data.
  @return M_chart The number of dimensions of the char data.
  """

  N = 0
  M_info = 0
  M_env = 0
  M_drv = 0
  M_chart = 0

  """
  Importing data
  and convert into pandas data fram
  """
  D = pd.read_csv(fname_in)
  df = pd.DataFrame(D)

  fields_info = [('rawdata_id', 1, 'id'), 
                 ('vehicle_id', 2, 'id'), 
                 ('driver_id', 3, 'id'), 
                 ('extract_start_date', 4, 'date')]

  fields_env = [('totaldistance', 5, 'scalar'),
                ('weight', 6, 'scalar'),
                ('weight_calculation_type', 7, 'class'), 
                ('traffic_index', 30, 'scalar'),
                ('H', 42, 'scalar'),
                ('S', 43, 'scalar'),
                ('L', 44, 'scalar'),
                ('pos_h', 45, 'scalar'),
                ('pctg_pos_h', 46, 'scalar'),
                ('std_dh', 47, 'scalar'),
                ('std_h', 48, 'scalar'),
                ('wt_deg_s', 49, 'scalar'),
                ('wt_deg_l', 50, 'scalar'),
                ('wt_sd_speed_l', 51, 'scalar'),
                ('wt_sd_altitude_l', 52, 'scalar'),
                ('wt_sd_speed_s', 53, 'scalar'),
                ('wt_sd_altitude_s', 54, 'scalar'),
                ('wt_ratio_time_all', 55, 'scalar'),
                ('wt_ratio_time_moving', 56, 'scalar'),
                ('wt_ratio_dist', 57, 'scalar'),
                ('highway_index_t', 58, 'scalar'),
                ('highway_index_t_moving', 59, 'scalar'),
                ('highway_index_s', 60, 'scalar'),
                ('avg_temp', 74, 'scalar'),
                ('avg_std_speed_flag_highway', 75, 'scalar'),
                ('time_on_flag_highway', 76, 'scalar')]
  
  fields_drv = [('overrpmtime', 11, 'scalar'),
                ('overomcount', 12, 'scalar'),
                ('overrpmmax', 13, 'scalar'),
                ('overspeedtime', 14, 'scalar'),
                ('overspeedcount', 15, 'scalar'),
                ('overspeedmax', 16, 'scalar'),
                ('shortwarmcount', 17, 'scalar'),
                ('shortcoolcount', 18, 'scalar'),
                ('excessspeedtime', 21, 'scalar'),
                ('coastoutofgeartime', 22, 'scalar'),
                ('ignitionviolationcount', 23, 'scalar'),
                ('CruiseCtrlTime', 27, 'scalar'),
                ('TopGearTime', 28, 'scalar'),
                ('excess_vs_overspeed', 29, 'scalar'),
                ('cab_style', 33, 'class'),
                ('tractor_manufacturer', 34, 'class'),
                ('make', 35, 'class'),
                ('model_year', 36, 'class'),
                ('tractor_model', 37, 'class'),
                ('engine_manufacturer', 38, 'class'),
                ('engine_series', 39, 'class'),
                ('engine_style', 40, 'class'),
                ('engine_capacity2', 41, 'class'),
                ('prog_shift_t', 64, 'scalar'),
                ('prog_shift_s', 65, 'scalar'),
                ('overrpm_t', 66, 'scalar'),
                ('overrpm_s', 67, 'scalar'),
                ('overspeed_t', 68, 'scalar'),
                ('overspeed_s', 69, 'scalar'),
                ('excessspeed_t', 70, 'scalar'),
                ('excessspeed_s', 71, 'scalar'),
                ('highway_topgear_t', 72, 'scalar'),
                ('highway_topgear_s', 73, 'scalar')]

  fields_chart = [('drivingtime', 8, 'scalar'),
                 ('enginetime', 9, 'scalar'),
                 ('intertripidletime', 10, 'scalar'),
                 ('movingtime', 19, 'scalar'),
                 ('shortidletime', 20, 'scalar'),
                 ('totalfuel', 24, 'scalar'),
                 ('idlefuel', 25, 'scalar'),
                 ('ParkedIdleFuel', 26, 'scalar'),
                 ('mpg_moving', 31, 'scalar'),
                 ('total_mpg', 32, 'scalar'),
                 ('matrix_sum_dist', 61, 'scalar'),
                 ('matrix_sum_t', 62, 'scalar'),
                 ('matrix_sum_t_moving', 63, 'scalar')]
  """
  Process the data (as a data frame)
  Output is a numpy array
  Feature(:, __feature_col__), Feature_class(:, __feature_class__)
  """

  
  """
  Step 1: extract the column information related to respective field types and store in 
  __field_type___cols = [...]
  """
  info_cols = []
  for feature_info in range(0, len(fields_info)):
      info_cols.append(fields_info[feature_info][1] - 1) 
  
  env_cols = []
  for feature_info in range(0, len(fields_env)):
      env_cols.append(fields_env[feature_info][1] - 1) 
  
  drv_cols = []
  for feature_info in range(0, len(fields_drv)):
      drv_cols.append(fields_drv[feature_info][1] - 1) 
  
  chart_cols = []
  for feature_info in range(0, len(fields_chart)):
      chart_cols.append(fields_chart[feature_info][1] - 1) 
  
  """
  Step2: Extract the data corresponding to the respective feature of a specific field type
  """
  Examples_info = df[df.columns[info_cols]]
  Examples_env = df[df.columns[env_cols]]
  Examples_drv = df[df.columns[drv_cols]]
  Examples_chart = df[df.columns[chart_cols]]


  """
  Step3: Calculate the mean and the standard deviation corresponding to the each 
  of the Examples_field other than info - only on features that have been marked as scalars.
  For non-scalar feautres perform one hot encoding. 

  @output - data_field (numpy array)
  """

  #pdb.set_trace()
  data_info = process_fields(Examples_info, fields_info)
  data_env = process_fields(Examples_env, fields_env)
  data_drv = process_fields(Examples_drv, fields_drv)
  data_chart = process_fields(Examples_chart, fields_chart)

  N = (data_env.shape[0] + 
          data_drv.shape[0] + data_chart.shape[0] + data_info.shape[0])/4
  
  if N != df.shape[0]:
      print("Number of examples post processing are more than the input")
      pdb.set_trace()

  M_env = data_env.shape[1]
  M_drv = data_drv.shape[1]
  M_chart = data_chart.shape[1]
  M_info = data_info.shape[1]

  #pdb.set_trace()

  
  """
  for i in range(0, len(Examples.columns)):                                                                                                      
    col = np.array( [((Examples[Examples.columns[i]] - Examples_mean[i])/ Examples_std_dev[i]).as_matrix()] ).T
   .....:     A = np.hs
np.hsplit  np.hstack  
   .....:     A = np.hstack((A,col))
  """
  """
  Step4: Save the data as numpy arrays
  fname_out_info, fname_out_env, fname_out_drv, fname_out_chart
  """
  np.save(fname_out_info, data_info)
  np.save(fname_out_env, data_env)
  np.save(fname_out_drv, data_drv)
  np.save(fname_out_chart, data_chart)

  
  # TODO: implementation

  return (N, M_info, M_env, M_drv, M_chart)

"""
Process the respective field vectors
If field_vector_type is a scalar then performs normalization
If field vector type is a class then perform one hot encoding
"""
def process_fields (Examples, field):
  """
  Initialize an empty zero vector to help with the hporizontal stack.
  """
  data_info = np.empty((Examples.shape[0],1))
  for i in range(0, len(Examples.columns)):
      if field[i][2] == 'scalar':
          vector = Examples[Examples.columns[i]]
          mean = vector.mean()
          sigma = vector.std()
          """
          Mahalanobis Normalization
          """
          norm_vector = np.array([((vector - mean)/sigma).as_matrix()]).T
          
          data_info = np.hstack((data_info, norm_vector))
      
      elif field[i][2] == 'class':
          vector = Examples[Examples.columns[i]]
          classes_list = list(set(Examples[Examples.columns[i]]))

          for item in range(0, len(classes_list)):
              col = np.zeros(vector.shape)
              one_hot_encoded_feature = classes_list[item]

              for element in range(0, len(col)):
                  if vector[element] == one_hot_encoded_feature:
                      col[element] = 1

              norm_vector = np.array([col]).T
              """
              stacl each of the newly generated <<one hot encoded vector>>
              """
              data_info = np.hstack((data_info, norm_vector))
      else:
          vector = np.array([Examples[Examples.columns[i]].as_matrix()]).T
          data_info = np.hstack((data_info, vector))
  """
  When returning discard the initialized empty zero vector
  """
  return data_info[:,1:]




def main():
  fname_in = '../data/driver_behavior.csv'
  fname_out_info = '../data/info.npy' # TODO: output file name
  fname_out_env = '../data/env.npy' # TODO: output file name
  fname_out_drv = '../data/drv.npy' # TODO: output file name
  fname_out_chart = '../data/chart.npy' # TODO: output file name

  N, M_info, M_env, M_drv, M_chart = proc_data(fname_in, fname_out_info, fname_out_env, \
          fname_out_drv, fname_out_chart)

  print('data has been processed (N=%d, M_info=%d, M_env=%d, M_drv=%d, M_char=%d)' % (N, M_info, \
          M_env, M_drv, M_chart))
  print('processed info data file saved (file: %s)' % (fname_out_info))
  print('processed environment data file saved (file: %s)' % (fname_out_env))
  print('processed driver data file saved (file: %s)' % (fname_out_drv))
  print('processed trip characteristic data file saved (file: %s)' % (fname_out_chart))


if __name__ == '__main__':
  main()
