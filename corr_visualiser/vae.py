import numpy as np

from keras.layers import Input, Dense, Lambda, Layer, LSTM, Dropout
from keras.models import Model
from keras.optimizers import Adam
from keras import backend as K
from keras import metrics
import tensorflow as tf
from tensorflow import keras
import copy

np.random.seed = 50
tf.random.set_seed(50)
latent_dim = 1

# Each sample will be of size 365 -> train dataset in batches of 365 -> predict annually
SAMPLE_SIZE = 365

EPOCHS = 300
BATCH_SIZE = 32
LOSS_FUNCTION = 'mse'
OPTIMIZER = Adam(lr=0.01)

training_set = {}
testing_set = {}
high_train_set = {}
high_test_set = {}
vae_list = {}
simulated = {}


class Vae:

    def __init__(self, stock_data):
        super().__init__()
        self.stock_data = stock_data

    '''
        Split the whole data set into training and testing sets
        - Original Dataset - 4755 data points
        - Training Set -> 80% of the original dataset -> 3084 data points
        - Test/Validation Set -> Remaining 20% of the original dataset -> 951 data point

        - Generate Training samples -> # 10 rows x 365 columns (21, 365)
        - Generate Testing samples -> # 2 row x 365 columns (1, 365)
    '''

    def split_dataset(self):
        print('===== Spliting Dataset =====')

        original_data_points = self.stock_data[0].shape[0]
        test_data_points = original_data_points//5
        test_data_points = 365
        print('original size: {}'.format(original_data_points))
        print('training size: {}'.format(test_data_points))
        print('testing size: {}'.format(original_data_points - test_data_points))

        high = self.stock_data[0]
        high_train = high[0:high.shape[0] - test_data_points]
        high_test = high[-test_data_points:]

        x_train = Vae.generate_samples(high_train, SAMPLE_SIZE)
        x_test = Vae.generate_samples(high_test, SAMPLE_SIZE)

        print('high train: {}'.format(high_train.shape))
        print('high test: {}'.format(high_test.shape))
        print('x train: {}'.format(x_train.shape))
        print('x test: {}'.format(x_test.shape))

        return x_train, x_test

        # training_set[code] = x_train
        # testing_set[code] = x_test

        # high_train_set[code] = high_train
        # high_test_set[code] = high_test

        # return high_train_set, high_test_set, training_set, testing_set

    '''
        Split training and testing datasets into smaller samples.

        Return a 2D array of smaller samples
            - rows: number of samples
            - column: sample size
    '''
    @classmethod
    def generate_samples(cls, data, sample_size):
        n_samples = data.shape[0]//sample_size  # Floor division
        result = np.empty((n_samples, sample_size))
        for i in range(n_samples):
            # n_sample rows x sample_size columns
            result[i] = data[i*sample_size: i*sample_size + sample_size]
        return result

    '''
        VAE = Encoder -> Decoder
        * add latent loss
        * compile with
            - loss: mse
            - optimizer: adam (learning_rate=0.01)
            - metrics: mse
    '''

    def build_model(self):
        self.build_encoder()
        self.build_decoder()

        _, _, sample = self.encoder(self.inputs)
        reconstructions = self.decoder(sample)
        variational_ae = Model(inputs=[self.inputs], outputs=[reconstructions])
        latent_loss = -0.5 * K.sum(
            1 + self.latent_log_var -
            K.exp(self.latent_log_var) - K.square(self.latent_mean),
            axis=-1)
        variational_ae.add_loss(K.mean(latent_loss)/(SAMPLE_SIZE*1.0))
        variational_ae.compile(loss=LOSS_FUNCTION,
                               optimizer=OPTIMIZER,
                               metrics=['mse'])

        self.variational_ae = variational_ae
        print(self.variational_ae.summary())
        # self.temp = []
        # for code in self.processed_data:
        #     vae_list[code] = variational_ae
        #     self.temp.append(vae_list[code])

        # print('same???? {}'.format(self.temp[0] == self.temp[1]))

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

    def build_encoder(self):
        inputs = Input(shape=[SAMPLE_SIZE])
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

        self.inputs = inputs
        self.latent_mean = latent_mean
        self.latent_log_var = latent_log_var
        self.encoder = variational_encoder

    '''
        ===== Decoder =====
        Input    (None, 1)      -> 
        Dense    (None, 16)     -> 
        Dense    (None, 32)     -> 
        Dense    (None, 128)    ->
        Dense    (None, 256)    ->
        Dense    (None, 365)
    '''

    def build_decoder(self):
        decoder_inputs = Input(shape=[latent_dim])
        x = Dense(16, activation='relu')(decoder_inputs)
        x = Dense(32, activation='relu')(x)
        x = Dense(128, activation='relu')(x)
        x = Dense(256, activation='relu')(x)
        outputs = Dense(SAMPLE_SIZE, activation='tanh')(x)
        variational_decoder = Model(inputs=[decoder_inputs], outputs=[outputs])

        self.decoder = variational_decoder

    '''
        Training the model
        * epochs: 300
        * batch_size: 32
        * no training labels 
    '''

    def train_model(self, training_set):
        print('===== Training Model =====')

        history = self.variational_ae.fit(
            training_set, training_set, epochs=EPOCHS, batch_size=BATCH_SIZE)

    '''
        Simulations
        - Predict
        - Save simulated result
    '''

    def simluate(self, testing_set):
        print('===== Predicting =====')

        simulated_high = np.empty(
            (testing_set.shape[0], SAMPLE_SIZE))
        print(simulated_high.shape)
        print(testing_set)
        print(testing_set[0].shape)
        print(testing_set[0].reshape(-1,1).shape)
        print(testing_set[0].reshape(1,-1).shape)
        for i in range(testing_set.shape[0]):
            simulated_high[i] = self.variational_ae.predict(testing_set[i].reshape(1,-1))

        return simulated_high


class Sampling(Layer):
    def call(self, inputs):
        mean, log_var = inputs
        # Return normal distribution of values, taking the shape of log_var
        # MULTIPLE by element-wise exponential of (log_var/2)
        # ADD the mean
        return K.random_normal(tf.shape(log_var)) * K.exp(log_var / 2) + mean
