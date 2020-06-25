import matplotlib.pyplot as plt
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import quandl

from keras.layers import Input, Dense, Lambda, Layer, LSTM, Dropout
from keras.models import Model
from keras.optimizers import Adam
from keras import backend as K
from keras import metrics
import tensorflow as tf
from tensorflow import keras
import pandas as pd
import os
import datetime

''' 
    Interested in stocks between 2010-06-01 to present
    Once off operations to obtain stocks data
'''
quandl.ApiConfig.api_key = "Z98DtXh7GAhy8vp_ucZW"
quandl_data = {}
is_first_time = False
is_debugging = False

if is_first_time:
    metadata = pd.read_csv('EOD_metadata.csv', delimiter=',')
    to_date = metadata['to_date']
    from_date = metadata['from_date']
    interested_stocks = metadata[(
        to_date > '2020-06-01') & (from_date < '2000-06-01')]
    stock_codes = interested_stocks['code'].values.tolist()

    if True:
        for code in stock_codes:
            product = 'WIKI/' + code
            try:
                data = quandl.get(product)
                print(product)
                pd.DataFrame(data).to_csv("wiki/{}_data.csv".format(code))
                quandl_data[code] = data
            except:
                print("Skip " + product)

'''
    If is not first time, parse data in via reading the csv
    Only interested in High Price
    Rename the column names from HIGH to PRODUCT HIGH
    Inner join on the same dates
'''
# ===== Whole Market =====
dataset = []
counter = 0
if not is_first_time and not is_debugging:
    dir = 'wiki/'
    files = []
    for _, _, f in os.walk(dir):
        for file in f:
            if '.csv' in file:
                if counter > 100:
                    break
                print('file: {}'.format(file))
                df = pd.read_csv('wiki/{}'.format(file),
                         delimiter=',', usecols=['Date', 'High'])
                code = os.path.splitext(file)[0].replace('_data','')
                print('code: {}'.format(code))
                quandl_data[code] = df
                counter += 1
    # cache
    np.save('stocks_data.npy', quandl_data)

if (is_debugging):
    quandl_data = np.load('stocks_data.npy', allow_pickle=True).item()

to_del = []
for code in quandl_data:
    df = quandl_data[code]
    first_date = pd.to_datetime(df['Date'][0])
    if (first_date < datetime.date(2000, 6, 1)):
        df.set_index('Date',inplace=True)
        df.rename(columns={'High': '{} High'.format(code)}, inplace=True)
        dataset.append(df)
    else:
        to_del.append(code)

# Delete outliers
for item in to_del:
    del quandl_data[item]

print('===== Merging stocks =====')
merged_df = pd.concat(dataset, join='inner', axis=1)
print(merged_df)

''' 
    Process Raw Data
    - Convert interested column into a numpy array of 1 row x _ columns -> [[1,2,3,...]]
    - Normalise the interested dataset via x/max(x)
    - Convert noramlised data into a list -> [1,2,3,...]
    - Find MAX of the normalised data

    - Save the raw interested dataset
    - Save the normalised interested dataset
'''
print('===== Processing Raw Stocks Data =====')
processed_data = { }
for code in quandl_data:
    high_raw = (merged_df['{} High'.format(code)].values).reshape(1, -1)
    high = preprocessing.normalize(high_raw, norm='max', axis=1)
    high = high.reshape(high.shape[1],)
    max_high = np.max(high_raw)
    processed_data[code] = (high, max_high)

def generate_samples(data, sample_size):
    n_samples = data.shape[0]//sample_size  # Floor division
    result = np.empty((n_samples, sample_size))
    for i in range(n_samples):
        # n_sample rows x sample_size columns
        result[i] = data[i*sample_size: i*sample_size + sample_size]
    return(result)


''' 
    Total: 8076 data points
    Training: 8076 - 365 = 7711
    Test/Val: 365
'''
test_data_points = 365
sample_size = 365


'''
    Split Data Set
    - Training Set -> 80% of the original dataset
    - Test/Validation Set -> Remaining 20% of the original dataset

    - Generate Training samples -> # 21 rows x 365 columns (21, 365)
    - Generate Testing samples -> # 1 row x 365 columns (1, 365)
'''
# ===== Whole Market =====
print('===== Spliting Dataset =====')
training_set = {}
testing_set = {}
for code in processed_data:
    high = processed_data[code][0]
    high_train = high[0:high.shape[0] - test_data_points]
    high_test = high[-test_data_points:]

    x_train = generate_samples(high_train, sample_size)
    x_test = generate_samples(high_test, sample_size)

    training_set[code] = x_train
    testing_set[code] = x_test

'''
    Building Model
    - VAE: Encoder -> Sampling -> Decoder
'''
np.random.seed = 50
tf.random.set_seed(50)
latent_dim = 1


class Sampling(Layer):
    def call(self, inputs):
        mean, log_var = inputs
        # Return normal distribution of values, taking the shape of log_var
        # MULTIPLE by element-wise exponential of (log_var/2)
        # ADD the mean
        return K.random_normal(tf.shape(log_var)) * K.exp(log_var / 2) + mean


'''
    ===== Encoder =====
    Input    (None, 365) -> 
    Dense    (None, 256) -> Dropout  (None, 256) -> 
    Dense    (None, 128) -> Dropout  (None, 128) -> 
    Dense    (None, 32)  ->
    Dense    (None, 16)  ->
    { Dense    (None, 1)   &&  Dense    (None, 1) } ->
    Sampling (?, 1)
'''
inputs = Input(shape=[sample_size])
z = Dense(256, activation='relu')(inputs)
z = Dropout(0.1)(z)
z = Dense(128, activation='relu')(z)
z = Dropout(0.1)(z)
z = Dense(32, activation='relu')(z)
z = Dense(16, activation='relu')(z)
latent_mean = Dense(latent_dim)(z)
latent_log_var = Dense(latent_dim)(z)
sample = Sampling()([latent_mean, latent_log_var])
variational_encoder = Model(inputs=[inputs], outputs=[
    latent_mean, latent_log_var, sample])

'''
    ===== Decoder =====
    Input    (None, 1)      -> 
    Dense    (None, 16)     -> 
    Dense    (None, 32)     -> 
    Dense    (None, 128)    ->
    Dense    (None, 256)    ->
    Dense    (None, 365)
'''
decoder_inputs = Input(shape=[latent_dim])
x = Dense(16, activation='relu')(decoder_inputs)
x = Dense(32, activation='relu')(x)
x = Dense(128, activation='relu')(x)
x = Dense(256, activation='relu')(x)
outputs = Dense(sample_size, activation='tanh')(x)
variational_decoder = Model(inputs=[decoder_inputs], outputs=[outputs])

'''
    VAE = Encoder -> Decoder
    * add latent loss
    * compile with
        - loss: mse
        - optimizer: adam (learning_rate=0.01)
        - metrics: mse
'''
_, _, sample = variational_encoder(inputs)
reconstructions = variational_decoder(sample)
variational_ae = Model(inputs=[inputs], outputs=[reconstructions])
latent_loss = -0.5 * K.sum(
    1 + latent_log_var - K.exp(latent_log_var) - K.square(latent_mean),
    axis=-1)
variational_ae.add_loss(K.mean(latent_loss)/(sample_size*1.))
variational_ae.compile(loss='mse',
                       optimizer=Adam(lr=0.01),
                       metrics=['mse'])


'''
    Training the model
    * epochs: 300
    * batch_size: 32
    * no training labels 
'''
# ===== Whole Market =====
print('===== Training Model =====')
vae_market = variational_ae
counter = 0
for code in quandl_data:
    # if counter > 10:
    #     break
    history = vae_market.fit(training_set[code], training_set[code], epochs=300, batch_size=32)
    counter += 1

'''
    Simulations
    - Predict
    - Save simulated result
'''
# ===== Whole Market =====
simulated = {}
for code in quandl_data:
    simulated_high = np.empty((testing_set[code].shape[0], sample_size))
    for i in range(testing_set[code].shape[0]):
        simulated_high[i] = vae_market.predict(testing_set[code][[i]])

    simulated[code] = simulated_high

'''
    Plot simulation graph
'''
# ===== Whole Market =====
real_data = {}
simulated_data = {}
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 9))
fig.suptitle('Last 365 days of Stock Data')
for code in quandl_data:
    max_high = processed_data[code][1]
    x_test = testing_set[code]
    simulated_high = simulated[code]

    real_high = max_high * x_test.flatten()
    simulated_high = max_high * simulated_high.flatten()
    real_data[code] = real_high
    simulated_data[code] = simulated_high

    ax1.plot(max_high * x_test.flatten(), label='{} Real Data'.format(code))
    ax2.plot(max_high * simulated_high.flatten(),label='{} Simulated Data'.format(code))

ax1.set(xlabel='Days', ylabel='High Prices')
ax2.set(xlabel='Days', ylabel='High Prices')
ax1.set_ylim([-1000,10000])
ax2.set_ylim([-1000,10000])
ax1.set_title('Real Data')
ax2.set_title('Simulated Data')
plt.show()

corr_real_data = {}
corr_simulated_data = {}
for code in quandl_data:
    corr_real_data['{} High'.format(code)] = real_data[code]
    corr_simulated_data['{} High Simulated'.format(code)] = simulated_data[code]

corr_real_df = pd.DataFrame(data=corr_real_data)
corr_simulated_df = pd.DataFrame(data=corr_simulated_data)
combined_data = corr_real_data.update(corr_simulated_data)
corr_total_df = pd.DataFrame(data=combined_data)

print(corr_real_df.corr())
corr_real_df.corr().to_csv('corr_real.csv')

print(corr_simulated_df.corr())
corr_simulated_df.corr().to_csv('corr_simulated.csv')

print(corr_total_df.corr())
corr_total_df.corr().to_csv('corr_total.csv')
