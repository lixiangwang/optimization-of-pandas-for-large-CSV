# encoding: utf-8
"""
@author:  wanglixiang
@contact: lixiangwang9705@gmail.com
"""


import numpy as np
import pandas as pd
import time


class reduce_fastload:
    def __init__(self, data_dir, use_HDF5=False, use_feather=False):
        """
        :use HDF5 to store: use_HDF5=True
        :use feather to store: use_feather=True
        
        """
        self.data_dir = data_dir
        self.use_HDF5 = use_HDF5
        self.use_feather = use_feather
        self.is_reduce = 0

    def reduce_data(self):
        df = pd.read_csv(self.data_dir, parse_dates=True, keep_date_col=True)

        start_mem = df.memory_usage().sum() / 1024 ** 2
        print('Memory usage of dataframe is {:.2f} MB'.format(start_mem))

        ## Reference from: https://www.kaggle.com/arjanso/reducing-dataframe-memory-size-by-65
        for col in df.columns:
            col_type = df[col].dtype

            if col_type != object:
                c_min = df[col].min()
                c_max = df[col].max()
                if str(col_type)[:3] == 'int':
                    if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                        df[col] = df[col].astype(np.int8)
                    elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                        df[col] = df[col].astype(np.int16)
                    elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                        df[col] = df[col].astype(np.int32)
                    elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                        df[col] = df[col].astype(np.int64)
                else:
                    if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                        df[col] = df[col].astype(np.float16)
                    elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                        df[col] = df[col].astype(np.float32)
                    else:
                        df[col] = df[col].astype(np.float64)
            else:

                df[col] = df[col].astype('category')

        end_mem = df.memory_usage().sum() / 1024 ** 2
        print('Memory usage after optimization is: {:.2f} MB'.format(end_mem))
        print('Decreased by {:.1f}%'.format(100 * (start_mem - end_mem) / start_mem))

        if self.use_HDF5 == True and self.use_feather == False:
            data_store = pd.HDFStore('processed_data.h5')
            # Store object in HDFStore
            data_store.put('preprocessed_df', df, format='table')

            data_store.close()
            self.is_reduce = 1
        elif self.use_HDF5 == False and self.use_feather == True:
            df.to_feather('processed_data.feather')
            self.is_reduce = 1
        else:
            print('Please choose the only way to compress：True or False')

    def reload_data(self):
        if self.is_reduce == 0:
            print('You have not compressed the data yet')

        else:
            if self.use_HDF5 == True and self.use_feather == False:

                time_start = time.time()
                store_data = pd.HDFStore('processed_data.h5')
                # 通过key获取数据
                preprocessed_df = store_data['preprocessed_df']
                print('load time:',time.time() - time_start)
                store_data.close()

            elif self.use_HDF5 == False and self.use_feather == True:
                time_start = time.time()
                preprocessed_df = pd.read_feather('processed_data.feather')
                print('load time:',time.time() - time_start)

            else:
                print('Please choose the only way to compress：True or False')

        return preprocessed_df