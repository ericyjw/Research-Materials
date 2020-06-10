import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

from keras.layers import Input, Dense, Lambda, Layer, LSTM
from keras.models import Model
from keras import backend as K
from keras import metrics
import tensorflow as tf

'''
  dataset: the set of data used
  target: the column of the data set (the column interested to predict)
  start_index: the start index on the dataset
  end_index: the end index of the dataset
  history_size: the size of information to look back to for prediction
  target_size: the size of the information to predict
  step: the number of steps taking
'''
def multivariate_data(dataset, target, start_index, end_index, history_size,
                      target_size, step, single_step=False):
    data = []
    labels = []

    start_index = start_index + history_size
    if end_index is None:
        end_index = len(dataset) - target_size

    for i in range(start_index, end_index):
        indices = range(i-history_size, i, step)
        data.append(dataset[indices])

        if single_step:
            labels.append(target[i+target_size])
        else:
            labels.append(target[i:i+target_size])

    return np.array(data), np.array(labels)


def create_time_steps(length):
    return list(range(-length, 0))


def show_plot(plot_data, delta, title):
    labels = ['History', 'True Future', 'Model Prediction']
    marker = ['.-', 'rx', 'go']
    time_steps = create_time_steps(plot_data[0].shape[0])
    if delta:
        future = delta
    else:
        future = 0

    plt.title(title)
    for i, x in enumerate(plot_data):
        if i:
            plt.plot(future, plot_data[i], marker[i], markersize=10,
                     label=labels[i])
        else:
            plt.plot(time_steps, plot_data[i].flatten(
            ), marker[i], label=labels[i])
    plt.legend()
    plt.xlim([time_steps[0], (future+5)*2])
    plt.xlabel('Time-Step')
    plt.show()
    return plt


def multi_step_plot(history, true_future, prediction):
    plt.figure(figsize=(12, 6))
    num_in = create_time_steps(len(history))
    num_out = len(true_future)

    plt.plot(num_in, np.array(history[:, 1]), label='History')
    plt.plot(np.arange(num_out)/STEP, np.array(true_future), 'bo',
             label='True Future')
    if prediction.any():
        plt.plot(np.arange(num_out)/STEP, np.array(prediction), 'ro',
                 label='Predicted Future')
    plt.legend(loc='upper left')
    plt.show()


''' 
  Using the CSV data and the VAE, generate a graph that is similar to the original graph
  For simplicity, we will only consider Open, Close, High & Low data points.

  CSV file contain 5995 rows of information (2990 rows will be used for training, 3005 rows will be used for validation)

'''

''' Global Variables '''
TRAIN_SPLIT = 2990
BATCH_SIZE = 256
BUFFER_SIZE = 10000
EVALUATION_INTERVAL = 200
EPOCHS = 10

PAST_HISTORY = 200
FUTURE_TARGET = 20
STEP = 5

''' Step 1: Extract Data From CSV '''
df = pd.read_csv('data.csv', delimiter=',', usecols=[
                 'Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
df = df.sort_values('Date')
print(df.head())  # shape: (5995, 7)


''' Step 2: Process Data '''
# Extract interested data - Open, Close, High, Low
features_considered = ['Open', 'Close', 'High', 'Low']
features = df[features_considered]
features.index = df['Date']
print(features.head())
features.plot(subplots=True)
plt.show()

# Structure the data into data & labels
dataset = features.values
x_train_data, y_train_label = multivariate_data(dataset, dataset, 0,
                                                TRAIN_SPLIT, PAST_HISTORY,
                                                FUTURE_TARGET, STEP)
x_val_data, y_val_label = multivariate_data(dataset, dataset,
                                            TRAIN_SPLIT, None, PAST_HISTORY,
                                            FUTURE_TARGET, STEP)

print('DEGUG: Single window of past history : {}'.format(x_train_data[0].shape))
print('DEBUG: Target window to predict : {}'.format(y_train_label[0].shape))


''' Step 3: Convert Python List data to Dataset Object '''
train_data = tf.data.Dataset.from_tensor_slices((x_train_data, y_train_label))
train_data = train_data.cache().shuffle(BUFFER_SIZE).batch(BATCH_SIZE).repeat()

val_data = tf.data.Dataset.from_tensor_slices((x_val_data, y_val_label))
val_data = val_data.batch(BATCH_SIZE).repeat()


''' Step 4: Set up model '''
original_dim = x_train_data.shape[-2:]
intermediate_dim = 256
latent_dim = 2
epsilon_std = 1.0  # Full Exploitation

print('DEGUG: Original Dimension: {}'.format(original_dim))
print('DEGUG: Intermdiate Dimension: {}'.format(intermediate_dim))
print('DEGUG: Latent Dimension: {}'.format(latent_dim))

# Encoder
x = Input(shape=original_dim)
h = Dense(intermediate_dim, activation='relu')(x)
z_mean = Dense(latent_dim)(h)
z_log_var = Dense(latent_dim)(h)

def sampling(args):
    z_mean, z_log_var = args
    epsilon = K.random_normal(shape=(K.shape(z_mean)[0], latent_dim), mean=0.,
                              stddev=epsilon_std)
    return z_mean + K.exp(z_log_var / 2) * epsilon

z = Lambda(sampling, output_shape=(latent_dim,))([z_mean, z_log_var])


# Decoder
decoder_h = Dense(intermediate_dim, activation='relu')
decoder_mean = Dense(original_dim, activation='relu')
h_decoded = decoder_h(z)
print('DEGUG: h_decoder shape: {}'.format(h_decoded.shape))
x_decoded_mean = decoder_mean(h_decoded)

y = x_decoded_mean
vae = Model(x, y)
print('DEGUG: Model Summary: \n{}'.format(vae.summary()))

''' Step 5: Compile Model '''
vae.compile(optimizer='rmsprop', loss='mae')



''' Step 6: Train Model '''
vae_step_history = vae.fit(train_data, epochs=EPOCHS,
                              steps_per_epoch=EVALUATION_INTERVAL,
                              validation_data=val_data,
                              validation_steps=50)



''' Step 7: Project Latent Space '''
encoder = Model(x, z_mean)
x_test_encoded = encoder.predict(val_data, batch_size=BATCH_SIZE)