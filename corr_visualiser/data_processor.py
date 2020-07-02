import quandl
import pandas as pd
import numpy as np
import os
import datetime
from sklearn import preprocessing

quandl.ApiConfig.api_key = "Z98DtXh7GAhy8vp_ucZW"
quandl_data = {}

class DataProcessor:

    def __init__(self):
        super().__init__()

    ''' 
        Download all the stock data with 
        from date: at least 2000-06-01 &
        to date: at least 2020-06-01
        and save them in the wiki/ dir

        Return a map of stock code to stock data frame that fits the criteria
    '''
    def download_data_from_quandl(self):
        print('===== Download Quandl Stocks Data =====')
        metadata = pd.read_csv('EOD_metadata.csv', delimiter=',')
        to_date = metadata['to_date']
        from_date = metadata['from_date']
        interested_stocks = metadata[(
            to_date > '2020-06-01') & (from_date < '2000-06-01')]
        stock_codes = interested_stocks['code'].values.tolist()

        # Save stocks data into csv
        for code in stock_codes:
            product = 'WIKI/' + code
            try:
                data = quandl.get(product)
                print(product)
                pd.DataFrame(data).to_csv("wiki/{}_data.csv".format(code))
                quandl_data[code] = data
            except:
                print("Skip " + product)

        self.quandl_data = quandl_data


    '''
        Load the downloaded stocks data from wiki/ dir
        Load only x amount of data
        Cache the loaded stocks data in.npy

        Return a map of stock code to stock data frame that fits the criteria
    '''
    def load_data_from_csv(self, limit):
        print('===== Load Stocks Data From CSV=====')

        dir = 'wiki/'
        files = []
        counter = 0
        for _, _, f in os.walk(dir):
            for file in f:
                if '.csv' in file:
                    if counter >= limit:
                        break
                    print('file: {}'.format(file))
                    df = pd.read_csv('wiki/{}'.format(file),
                                    delimiter=',', usecols=['Date', 'High'])
                    code = os.path.splitext(file)[0].replace('_data', '')
                    print('code: {}'.format(code))
                    quandl_data[code] = df
                    counter += 1
        # cache
        np.save('stocks_data.npy', quandl_data)

        self.quandl_data = quandl_data


    
    '''
        Second filter stocks data with their first date before 2000-06-01
            - EOD_metadata has some error in their from_date
        Only interested in High-Price variable
        Rename the column names from HIGH to PRODUCT HIGH
        Inner join on the same dates

        Return a merged data frame of the combined stock data
            - rows: date
            - columns: stocks-high price
    '''
    def process_stocks_df(self):
        print('===== Rename Stocks Data Column =====')

        dataset = []
        to_del = []
        for code in quandl_data:
            df = quandl_data[code]
            first_date = pd.to_datetime(df['Date'][0])
            if (first_date < datetime.date(2000, 6, 1)):
                df.set_index('Date', inplace=True)
                df.rename(columns={'High': '{} High'.format(code)}, inplace=True)
                dataset.append(df)
            else:
                to_del.append(code)

        # Delete outliers
        for item in to_del:
            del quandl_data[item]

        print('===== Merge Stock Data Into Single Table =====')
        merged_df = pd.concat(dataset, join='inner', axis=1)
        print(merged_df)

        self.merged_df = merged_df

    ''' 
        Convert interested column into a numpy array of 1 row x _ columns -> [[1,2,3,...]]
        Normalise the interested dataset via x/max(x) -> axis 1 = normalise row
        Convert noramlised data into a list -> [1,2,3,...]
        Find MAX of the normalised data

        Save the raw interested dataset
        Save the normalised interested dataset

        Return a map of stock code to a tuple (normalised data, max of raw data)
    '''
    def process_raw_stocks_data(self):
        print('===== Process Raw Stocks Data =====')
        merged_df = self.merged_df

        processed_data = {}
        for code in quandl_data:
            code_high_raw = (merged_df['{} High'.format(code)].values).reshape(1, -1)
            code_high = preprocessing.normalize(code_high_raw, norm='max', axis=1)
            code_high = code_high.reshape(code_high.shape[1],)
            code_max_high = np.max(code_high_raw)
            processed_data[code] = (code_high, code_max_high)

        return processed_data