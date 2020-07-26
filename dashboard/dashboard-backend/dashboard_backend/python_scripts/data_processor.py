# import quandl
import pandas as pd
import json
import numpy as np
import os
import datetime
from sklearn import preprocessing


class DataProcessor:

    def __init__(self):
        super().__init__()

    def find_common_period(self, data):
        print('===== Process Javascript Data =====')

        # start_date = datetime.datetime(2000, 6, 1)
        # end_date = datetime.datetime(2020, 5, 1)

        dataset = []
        for d in data:
            filename = d['fileName'].split('_')[0].capitalize()

            json_obj = json.loads(d['data'])
            df = pd.DataFrame(json_obj)

            filtered = df
            # filtered = df[(pd.to_datetime(df['Date']) > start_date) & (pd.to_datetime(df['Date']) <= end_date)]

            if not filtered.empty:
                filtered.set_index('Date', inplace=True)

                new_col_name = filename + " High"
                filtered.rename(columns={'High': new_col_name}, inplace=True)

                filtered.dropna(inplace=True)
                # print(filtered)

                dataset.append(filtered[new_col_name])

        print('===== Merge Data Into Single Table =====')
        merged_df = pd.concat(dataset, join='inner', axis=1)

        start_date = merged_df.head(1).index.values[0]
        end_date = merged_df.tail(1).index.values[0]
        num_of_common_dates = merged_df.shape[0]

        return merged_df, json.dumps({"start_date": start_date, "end_date": end_date, "common": num_of_common_dates})

    def process_raw_data(self, merged_df, start_date, end_date):
        print('===== Process Raw Data =====')

        filtered = merged_df[(merged_df.index.to_series() > start_date) & (merged_df.index.to_series() <= end_date)]
        processed_data = {}
        columns = list(filtered.columns)
        for col in columns:
            high_raw = (filtered[col].values).reshape(1, -1)
            high = preprocessing.normalize(high_raw, norm='max', axis=1)
            high = high.reshape(high.shape[1],)
            max_high = np.max(high_raw)
            processed_data[col] = (high, max_high)

        return processed_data

