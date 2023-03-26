from keras import Sequential
from keras.callbacks import ModelCheckpoint
from keras.layers import *

from data_preprocess import preprocess_data, reshape_into_samples
import numpy as np

# Trains various architectures of networks. Networks and training history is saved in separate files

np.random.seed(1)

real_dataset = np.load("real_dataset/dataset.npy")
arti_dataset = np.loadtxt("artificial_dataset/myfile.csv", delimiter=",")

noised_train, original_train = preprocess_data(arti_dataset[10:50])
noised_test, original_test = preprocess_data(arti_dataset[0:10])

points_per_sample = 600

noised_train = reshape_into_samples(noised_train, points_per_sample=points_per_sample)
original_train = reshape_into_samples(original_train, points_per_sample=points_per_sample)

noised_test = reshape_into_samples(noised_test, points_per_sample=points_per_sample)
original_test = reshape_into_samples(original_test, points_per_sample=points_per_sample)

print("noised_train set: %s, original_train: %s" % (noised_train.shape, original_train.shape))

max_layers = 10
regularization_factor = 0.0000


def do_training(neurons_per_layer, layers):
    model = Sequential()

    model.add(LSTM(neurons_per_layer, return_sequences=True,  input_shape=(points_per_sample, 1),  kernel_regularizer=regularizers.l2(regularization_factor)))
    model.add(Dense(neurons_per_layer, activation='relu', kernel_regularizer=regularizers.l2(regularization_factor)) )
    model.add(LSTM(neurons_per_layer, return_sequences=True,  input_shape=(points_per_sample, 1),  kernel_regularizer=regularizers.l2(regularization_factor)))
    for i in range(0, layers):
        model.add(Dense(neurons_per_layer, activation='relu', kernel_regularizer=regularizers.l2(regularization_factor)) )
    model.add(Dense(1))


    model.compile(loss='mean_squared_error', optimizer="adam")
    model.summary()
    model.save('network history/network.00.hdf5')
    model.fit(noised_train, original_train, validation_data=(noised_test, original_test),
              epochs=50,
              callbacks=[ModelCheckpoint(filepath='network history/network.{epoch:02d}.hdf5')],
              batch_size=64, verbose=2)


do_training(140, 2)
