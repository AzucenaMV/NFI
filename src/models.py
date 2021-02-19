from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Dropout, Conv1D, Conv2D, MaxPool2D, MaxPool1D

def dense_model(n_classes):
    model = Sequential()
    model.add(Flatten())
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(32, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(16, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(n_classes, activation='sigmoid'))
    return model


def conv_model(n_labels):
    # should probably add more filters, but not sure how to choose it
    filter_s = 3
    kernelsize = 3
    poolsize = (3, 1)
    # can also flatten within layers
    model = Sequential()
    model.add(Conv1D(6, kernelsize, activation='relu'))
    model.add(Conv1D(6, kernelsize, activation='relu'))
    model.add(MaxPool2D(poolsize))
    model.add(Conv1D(6, kernelsize, activation='relu'))
    model.add(Conv1D(6, kernelsize, activation='relu'))
    model.add(MaxPool2D(poolsize))
    model.add(Flatten())
    model.add(Dense(50, activation='relu'))
    model.add(Dropout(rate=0.5))
    model.add(Dense(20, activation='relu'))
    model.add(Dense(n_labels, activation='sigmoid'))
    return model


def model_for_example(n_features, n_classes):
    model = Sequential()
    model.add(Dense(32, activation='relu', input_dim=n_features))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(n_classes, activation='sigmoid'))
    return model