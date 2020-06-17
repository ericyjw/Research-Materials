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
        # df.index = df['Date']
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


# ===== Specific stocks =====
quandl_data_apple = quandl.get('WIKI/AAPL')
quandl_data_amazon = quandl.get('WIKI/AMZN')
quandl_data_msft = quandl.get('WIKI/MSFT')  # 8076 rows x 12 columns

pd.DataFrame(quandl_data_msft).to_csv("raw/msft_data.csv")
pd.DataFrame(quandl_data_apple).to_csv("raw/apple_data.csv")
pd.DataFrame(quandl_data_amazon).to_csv("raw/amazon_data.csv")

quandl_data_apple.rename(columns={"High": "Apple High"}, inplace=True)
quandl_data_amazon.rename(columns={"High": "Amazon High"}, inplace=True)
quandl_data_msft.rename(columns={"High": "MSFT High"}, inplace=True)

dataset = [quandl_data_msft['MSFT High'], quandl_data_apple['Apple High'],
           quandl_data_amazon['Amazon High']]

df = pd.concat(dataset, join='inner', axis=1)

''' 
    Process Raw Data
    - Convert interested column into a numpy array of 1 row x _ columns -> [[1,2,3,...]]
    - Normalise the interested dataset via x/max(x)
    - Convert noramlised data into a list -> [1,2,3,...]
    - Find MAX of the normalised data

    - Save the raw interested dataset
    - Save teh normalised interested dataset
'''
# ===== Whole Market =====
print('===== Processing Raw Stocks Data =====')
processed_data = { }
for code in quandl_data:
    high_raw = (merged_df['{} High'.format(code)].values).reshape(1, -1)
    high = preprocessing.normalize(high_raw, norm='max', axis=1)
    high = high.reshape(high.shape[1],)
    max_high = np.max(high_raw)
    processed_data[code] = (high, max_high)

# ===== Specific stocks =====
# MSFT
# msft_high_raw = (quandl_data_msft['High'].values).reshape(1, -1)
msft_high_raw = (df['MSFT High'].values).reshape(1, -1)
msft_high = preprocessing.normalize(msft_high_raw, norm='max', axis=1)
msft_high = msft_high.reshape(msft_high.shape[1],)
msft_max_high = np.max(msft_high_raw)

np.savetxt('data/raw_msft_high.csv', msft_high_raw.reshape(-1, 1),
           header='MSFT High', delimiter=',', fmt='%f', comments='')
np.savetxt('data/normalised_msft_high.csv', msft_high.reshape(-1, 1),
           header='MSFT Normalised High', delimiter=',', fmt='%f', comments='')

# Apple
# apple_high_raw = (quandl_data_apple['High'].values).reshape(1, -1)
apple_high_raw = (df['Apple High'].values).reshape(1, -1)
apple_high = preprocessing.normalize(apple_high_raw, norm='max', axis=1)
apple_high = apple_high.reshape(apple_high.shape[1],)
apple_max_high = np.max(apple_high_raw)

np.savetxt('data/raw_apple_high.csv', apple_high_raw.reshape(-1, 1),
           header='Apple High', delimiter=',', fmt='%f', comments='')
np.savetxt('data/normalised_apple_high.csv', apple_high.reshape(-1, 1),
           header='Apple Normalised High', delimiter=',', fmt='%f', comments='')

# Amazon
# amazon_high_raw = (quandl_data_amazon['High'].values).reshape(1, -1)
amazon_high_raw = (df['Amazon High'].values).reshape(1, -1)
amazon_high = preprocessing.normalize(amazon_high_raw, norm='max', axis=1)
amazon_high = amazon_high.reshape(amazon_high.shape[1],)
amazon_max_high = np.max(amazon_high_raw)

np.savetxt('data/raw_amazon_high.csv', amazon_high_raw.reshape(-1, 1),
           header='Amazon High', delimiter=',', fmt='%f', comments='')
np.savetxt('data/normalised_amazon_high.csv', amazon_high.reshape(-1, 1),
           header='Amazon Normalised High', delimiter=',', fmt='%f', comments='')

# Average High -> MSFT + Apple + Amazon
min_col = np.min(
    [msft_high_raw.shape[1], amazon_high_raw.shape[1], apple_high_raw.shape[1]])
average_high_raw = (
    msft_high_raw[0, 0:min_col] + amazon_high_raw[0, 0:min_col] + apple_high_raw[0, 0:min_col]) / 3
average_high = preprocessing.normalize(
    average_high_raw.reshape(1, -1), norm='max', axis=1)
average_high = average_high.reshape(average_high.shape[1])
average_max_high = np.max(average_high)

np.savetxt('data/raw_average_high.csv', average_high_raw.reshape(-1, 1),
           header='Average High', delimiter=',', fmt='%f', comments='')
np.savetxt('data/normalised_average_high.csv', average_high.reshape(-1, 1),
           header='Average Normalised High', delimiter=',', fmt='%f', comments='')


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


# ===== Specific Stocks =====
# MSFT
msft_high_train = msft_high[0:msft_high.shape[0] -
                            test_data_points]  # 0 to 7711 (21 samples)
msft_high_test = msft_high[-test_data_points:]  # 7711 to 8076 (1 sample)
X_msft_train = generate_samples(msft_high_train, sample_size)
X_msft_test = generate_samples(msft_high_test, sample_size)

# Apple
apple_high_train = apple_high[0:apple_high.shape[0]-test_data_points]
apple_high_test = apple_high[-test_data_points:]
X_apple_train = generate_samples(apple_high_train, sample_size)
X_apple_test = generate_samples(apple_high_test, sample_size)

# Amazon
amazon_high_train = amazon_high[0:amazon_high.shape[0]-test_data_points]
amazon_high_test = amazon_high[-test_data_points:]
X_amazon_train = generate_samples(amazon_high_train, sample_size)
X_amazon_test = generate_samples(amazon_high_test, sample_size)

# Average High Price
average_high_train = average_high[0: average_high.shape[0] - test_data_points]
average_high_test = average_high[-test_data_points:]
X_average_train = generate_samples(average_high_train, sample_size)
X_average_test = generate_samples(average_high_test, sample_size)


'''
    Building Model
    - VAE: Encoder -> Sampling -> Decoder
'''
np.random.seed = 50
tf.random.set_random_seed(50)
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


# ===== Specific Stocks =====
# MSFT
vae_msft = variational_ae
history = vae_msft.fit(X_msft_train, X_msft_train, epochs=300, batch_size=32)

# Apple
vae_apple = variational_ae
history = vae_apple.fit(X_apple_train, X_apple_train,
                        epochs=300, batch_size=32)

# Amazon
vae_amazon = variational_ae
history = vae_amazon.fit(X_amazon_train, X_amazon_train,
                         epochs=300, batch_size=32)

# Average High
vae_average = variational_ae
history = vae_average.fit(
    X_average_train, X_average_train, epochs=300, batch_size=32)


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

# ===== Specific Stocks =====
# MSFT
msft_simulated_high = np.empty(
    (X_msft_test.shape[0], sample_size))  # 1 row x 365 columns (1, 365)
for i in range(X_msft_test.shape[0]):
    msft_simulated_high[i] = vae_msft.predict(X_msft_test[[i]])

np.savetxt('data/simulated_msft_high.csv', msft_simulated_high.reshape(-1, 1),
           header='MSFT Simulated High', delimiter=',', fmt='%f', comments='')

# Apple
apple_simulated_high = np.empty(
    (X_apple_test.shape[0], sample_size))  # 1 row x 365 columns (1, 365)
for i in range(X_apple_test.shape[0]):
    apple_simulated_high[i] = vae_apple.predict(X_apple_test[[i]])

np.savetxt('data/simulated_apple_high.csv', apple_simulated_high.reshape(-1, 1),
           header='Apple Simulated High', delimiter=',', fmt='%f', comments='')

# Amazon
amazon_simulated_high = np.empty(
    (X_amazon_test.shape[0], sample_size))  # 1 row x 365 columns (1, 365)
for i in range(X_amazon_test.shape[0]):
    amazon_simulated_high[i] = vae_amazon.predict(X_amazon_test[[i]])

np.savetxt('data/simulated_amazon_high.csv', amazon_simulated_high.reshape(-1, 1),
           header='Amazon Simulated High', delimiter=',', fmt='%f', comments='')

# Average High
average_simulated_high = np.empty(
    (X_average_test.shape[0], sample_size))  # 1 row x 365 columns (1, 365)
for i in range(X_average_test.shape[0]):
    average_simulated_high[i] = vae_average.predict(X_average_test[[i]])

np.savetxt('data/simulated_average_high.csv', average_simulated_high.reshape(-1, 1),
           header='Average Simulated High', delimiter=',', fmt='%f', comments='')

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
# ax1.legend(loc='upper left')
# ax2.legend(loc='upper left')
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

exit()

# ===== Specific Stocks =====
# ===== Last 365 Days of Stock Data =====
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 9))
fig.suptitle('Last 365 days of Stock Data')
# MSFT
iter_0_msft_real = msft_max_high * X_msft_test.flatten()
iter_0_msft_simulated = msft_max_high * msft_simulated_high.flatten()
ax1.plot(msft_max_high * X_msft_test.flatten(), label='MSFT Real Data')
ax1.plot(msft_max_high * msft_simulated_high.flatten(),
         label='MSFT Simulated Data')
ax1.legend(loc='upper left')
ax1.set(xlabel='Days', ylabel='High Prices')
ax1.set_title('MSFT')
# Apple
ax2.plot(apple_max_high * X_apple_test.flatten(), label='Apple Real Data')
ax2.plot(apple_max_high * apple_simulated_high.flatten(),
         label='Apple Simulated Data')
ax2.legend(loc='upper left')
ax2.set(xlabel='Days', ylabel='High Prices')
ax2.set_title('Apple')
# Amazon
ax3.plot(amazon_max_high * X_amazon_test.flatten(), label='Amazon Real Data')
ax3.plot(amazon_max_high * amazon_simulated_high.flatten(),
         label='Amazon Simulated Data')
ax3.legend(loc='upper left')
ax3.set(xlabel='Days', ylabel='High Prices')
ax3.set_title('Amazon')
# Average
ax4.plot(average_max_high * X_average_test.flatten(),
         label='Average Real Data')
ax4.plot(average_max_high * average_simulated_high.flatten(),
         label='Average Simulated Data')
ax4.legend(loc='upper left')
ax4.set(xlabel='Days', ylabel='High Prices')
ax4.set_title('Average')

# plt.savefig('results/last_365_days_stock_data.png', dpi=300)
# plt.show()

# ===== Whole Stock Data =====
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 9))
fig.suptitle('Whole Stock Data')
# MSFT
ax1.plot(msft_max_high * np.append(X_msft_train,
                                   X_msft_test).flatten(), label='MSFT Real Data')
ax1.plot(msft_max_high * np.append(msft_high_train, msft_simulated_high).flatten(),
         label='MSFT Simulated Data')
ax1.legend(loc='upper left')
ax1.set(xlabel='Days', ylabel='High Prices')
ax1.set_title('MSFT')
# Apple
ax2.plot(apple_max_high * np.append(X_apple_train,
                                    X_apple_test).flatten(), label='Apple Real Data')
ax2.plot(apple_max_high * np.append(apple_high_train, apple_simulated_high).flatten(),
         label='Apple Simulated Data')
ax2.legend(loc='upper left')
ax2.set(xlabel='Days', ylabel='High Prices')
ax2.set_title('Apple')
# Amazon
ax3.plot(amazon_max_high * np.append(X_amazon_train,
                                     X_amazon_test).flatten(), label='Amazon Real Data')
ax3.plot(amazon_max_high * np.append(amazon_high_train, amazon_simulated_high).flatten(),
         label='Amazon Simulated Data')
ax3.legend(loc='upper left')
ax3.set(xlabel='Days', ylabel='High Prices')
ax3.set_title('Amazon')
# Average
ax4.plot(average_max_high * np.append(X_average_train,
                                      X_average_test).flatten(), label='Average Real Data')
ax4.plot(average_max_high * np.append(average_high_train, average_simulated_high).flatten(),
         label='Average Simulated Data')
ax4.legend(loc='upper left')
ax4.set(xlabel='Days', ylabel='High Prices')
ax4.set_title('Average')

# plt.savefig('results/whole_stock_data.png', dpi=300)
# plt.show()


''' 
    Repeat for 100 iterations 
'''
simulated_msft = [iter_0_msft_simulated]
for i in range(100):
    history = vae_msft.fit(X_msft_train, X_msft_train,
                           epochs=300, batch_size=32)
    msft_simulated_high = np.empty(
        (X_msft_test.shape[0], sample_size))  # 1 row x 365 columns (1, 365)
    for i in range(X_msft_test.shape[0]):
        msft_simulated_high[i] = vae_msft.predict(X_msft_test[[i]])

    iter_simulated = msft_max_high * msft_simulated_high.flatten()
    simulated_msft.append(iter_simulated)

plt.figure(figsize=(21, 5))
plt.plot(msft_max_high * X_msft_test.flatten(),
         label='MSFT Real Data', linewidth=5)
for i in range(0, len(simulated_msft), 10):
    plt.plot(simulated_msft[i],
             label='MSFT Simulated Data Iteration {}'.format(i))
plt.legend(loc='best')
plt.show()

exit()
real_dataset = [msft_max_high * np.append(X_msft_train, X_msft_test).flatten(),
                apple_max_high *
                np.append(X_apple_train, X_apple_test).flatten(),
                amazon_max_high * np.append(X_amazon_train, X_amazon_test).flatten()]

simulated_dataset = [msft_max_high * np.append(msft_high_train, msft_simulated_high).flatten(),
                     apple_max_high *
                     np.append(apple_high_train,
                               apple_simulated_high).flatten(),
                     amazon_max_high *
                     np.append(amazon_high_train,
                               amazon_simulated_high).flatten(),
                     ]

print(real_dataset[0].shape[0])
print(simulated_dataset[0].shape[0])


df = pd.DataFrame(data={'MSFT High': real_dataset[0],
                        'Apple High': real_dataset[1],
                        'Amazon High': real_dataset[2],
                        'MSFT High Simulated': simulated_dataset[0][:real_dataset[0].shape[0]],
                        'Apple High Simulated': simulated_dataset[1][:real_dataset[1].shape[0]],
                        'Amazon High Simulated': simulated_dataset[2][:real_dataset[2].shape[0]]
                        })

print(df)

# exit()
# quandl_data_apple.rename(columns={"High": "Apple High"}, inplace=True)
# quandl_data_amazon.rename(columns={"High": "Amazon High"}, inplace=True)
# quandl_data_msft.rename(columns={"High": "MSFT High"}, inplace=True)

# dataset = [quandl_data_apple['Apple High'],
#            quandl_data_msft['MSFT High'], quandl_data_amazon['Amazon High']]

# df = pd.concat(dataset, join='inner', axis=1)
print(df)
print(type(df))
print(df.info())

df.plot(figsize=(20, 5))
plt.xlabel('Year')
plt.show()

df.rolling(20).mean().plot(figsize=(20, 5))
plt.xlabel('Year')
plt.show()

df.diff().plot(figsize=(20, 5))
plt.xlabel('Year')

print(df.corr())
df.corr().to_csv('corr.csv')
exit()
