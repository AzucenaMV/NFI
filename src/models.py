from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Input, Dense, Flatten, Dropout, Conv1D, Conv2D, MaxPool2D, MaxPool1D, \
    MaxPooling2D, UpSampling2D, concatenate
from tensorflow.keras.optimizers import Adam


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


def unet_from_aml(input_size=(6000, 5, 1)):
    inputs = Input(input_size)
    # Convolution 1
    kernelsize = (3, 5)     # all 5 dyes
    kernelsize_up = (2, 5)  # one less because concatenated
    poolsize = (2, 1)       # pooling

    conv1 = Conv2D(64, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(inputs)
    conv1 = Conv2D(64, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(conv1)
    # Pooling 1
    pool1 = MaxPooling2D(poolsize)(conv1)
    # Convolution 2
    conv2 = Conv2D(128, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(pool1)
    conv2 = Conv2D(128, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(conv2)
    # Pooling 2
    pool2 = MaxPooling2D(poolsize)(conv2)
    # Convolution 3
    conv3 = Conv2D(256, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(pool2)
    conv3 = Conv2D(256, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(conv3)
    # Pooling 3
    pool3 = MaxPooling2D(poolsize)(conv3)
    # Convolution 3
    conv4 = Conv2D(512, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(pool3)
    conv4 = Conv2D(512, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(conv4)
    # Dropout
    drop4 = Dropout(0.5)(conv4)
    # Pooling 4
    pool4 = MaxPooling2D(poolsize)(drop4)
    # Convolution 5
    conv5 = Conv2D(1024, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(pool4)
    conv5 = Conv2D(1024, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(conv5)
    # Dropout
    drop5 = Dropout(0.5)(conv5)
    # Upward Convolution 6
    up6 = Conv2D(512, kernelsize_up, activation='relu', padding='same',
                 kernel_initializer='he_normal'
                 )(UpSampling2D(poolsize)(drop5))
    # Here we copy the input from the upward convolution and contraction path
    merge6 = concatenate([drop4, up6])
    conv6 = Conv2D(512, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(merge6)
    conv6 = Conv2D(512, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(conv6)
    # Upward Convolution 7
    up7 = Conv2D(256, kernelsize_up, activation='relu', padding='same',
                 kernel_initializer='he_normal'
                 )(UpSampling2D(poolsize)(conv6))
    # Here we copy the input from the upward convolution and contraction path
    merge7 = concatenate([conv3, up7])
    conv7 = Conv2D(256, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(merge7)
    conv7 = Conv2D(256, kernelsize, activation='relu', padding='same', kernel_initializer='he_normal'
                   )(conv7)
    # Upward Convolution 8
    up8 = Conv2D(128, kernelsize_up, activation='relu', padding='same',
                 kernel_initializer='he_normal'
                 )(UpSampling2D(poolsize)(conv7))
    # Here we copy the input from the upward convolution and contraction path
    merge8 = concatenate([conv2, up8])
    conv8 = Conv2D(128, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(merge8)
    conv8 = Conv2D(128, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(conv8)
    # Upward Convolution 9
    up9 = Conv2D(64, kernelsize, activation='relu', padding='same',
                 kernel_initializer='he_normal'
                 )(UpSampling2D(poolsize)(conv8))
    # Here we copy the input from the upward convolution and contraction path
    merge9 = concatenate([conv1, up9])
    conv9 = Conv2D(64, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(merge9)
    conv9 = Conv2D(64, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(conv9)
    conv9 = Conv2D(2, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(conv9)
    # not sure what to do with this shape
    # want to end up with 1 filter right?
    conv10 = Conv2D(1, 1, activation='sigmoid')(conv9)
    model = Model(inputs=inputs, outputs=conv10)
    model.compile(optimizer=Adam(lr=1e-3), loss='binary_crossentropy', metrics=['AUC'])

    return model


def unet_small(input_size=(6000, 5, 1)):
    inputs = Input(input_size)
    # Convolution 1
    kernelsize = (3, 5)     # all 5 dyes
    kernelsize_up = (2, 5)  # one less because concatenated
    poolsize = (2, 1)       # pooling

    conv1 = Conv2D(2, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(inputs)
    conv1 = Conv2D(2, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(conv1)
    # Pooling 1
    pool1 = MaxPooling2D(poolsize)(conv1)
    # Convolution 2
    conv2 = Conv2D(4, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(pool1)
    conv2 = Conv2D(4, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(conv2)
    # Pooling 2
    pool2 = MaxPooling2D(poolsize)(conv2)
    # Convolution 3
    conv3 = Conv2D(8, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(pool2)
    conv3 = Conv2D(8, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(conv3)
    # Pooling 3
    pool3 = MaxPooling2D(poolsize)(conv3)
    # Convolution 3
    conv4 = Conv2D(16, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(pool3)
    conv4 = Conv2D(16, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(conv4)
    # Dropout
    drop4 = Dropout(0.5)(conv4)

    # Upward Convolution 7
    up7 = Conv2D(8, kernelsize_up, activation='relu', padding='same',
                 kernel_initializer='he_normal'
                 )(UpSampling2D(poolsize)(drop4))
    # Here we copy the input from the upward convolution and contraction path
    merge7 = concatenate([conv3, up7])
    conv7 = Conv2D(8, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(merge7)
    conv7 = Conv2D(8, kernelsize, activation='relu', padding='same', kernel_initializer='he_normal'
                   )(conv7)
    # Upward Convolution 8
    up8 = Conv2D(4, kernelsize_up, activation='relu', padding='same',
                 kernel_initializer='he_normal'
                 )(UpSampling2D(poolsize)(conv7))
    # Here we copy the input from the upward convolution and contraction path
    merge8 = concatenate([conv2, up8])
    conv8 = Conv2D(4, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(merge8)
    conv8 = Conv2D(4, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(conv8)
    # Upward Convolution 9
    up9 = Conv2D(2, kernelsize, activation='relu', padding='same',
                 kernel_initializer='he_normal'
                 )(UpSampling2D(poolsize)(conv8))
    # Here we copy the input from the upward convolution and contraction path
    merge9 = concatenate([conv1, up9])
    conv9 = Conv2D(2, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(merge9)
    conv9 = Conv2D(2, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(conv9)
    conv9 = Conv2D(2, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(conv9)
    # not sure what to do with this shape
    # want to end up with 1 filter right?
    conv10 = Conv2D(1, 1, activation='sigmoid')(conv9)
    model = Model(inputs=inputs, outputs=conv10)
    model.compile(optimizer=Adam(lr=1e-3), loss='binary_crossentropy', metrics=['AUC'])

    return model


def unet_tiny(input_size=(120, 5, 1)):
    inputs = Input(input_size)
    # Convolution 1
    kernelsize = (3, 5)     # all 5 dyes
    kernelsize_up = (2, 5)  # one less because concatenated
    poolsize = (2, 1)       # pooling

    conv1 = Conv2D(2, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(inputs)
    conv1 = Conv2D(2, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(conv1)
    # Pooling 1
    pool1 = MaxPooling2D(poolsize)(conv1)
    # Convolution 2
    conv2 = Conv2D(4, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(pool1)
    conv2 = Conv2D(4, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(conv2)
    # Pooling 2
    pool2 = MaxPooling2D(poolsize)(conv2)
    # Convolution 3
    conv3 = Conv2D(8, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(pool2)
    conv3 = Conv2D(8, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(conv3)

    # Dropout
    drop4 = Dropout(0.5)(conv3)


    # Upward Convolution 8
    up8 = Conv2D(4, kernelsize_up, activation='relu', padding='same',
                 kernel_initializer='he_normal'
                 )(UpSampling2D(poolsize)(drop4))
    # Here we copy the input from the upward convolution and contraction path
    merge8 = concatenate([conv2, up8])
    conv8 = Conv2D(4, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(merge8)
    conv8 = Conv2D(4, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(conv8)
    # Upward Convolution 9
    up9 = Conv2D(2, kernelsize, activation='relu', padding='same',
                 kernel_initializer='he_normal'
                 )(UpSampling2D(poolsize)(conv8))
    # Here we copy the input from the upward convolution and contraction path
    merge9 = concatenate([conv1, up9])
    conv9 = Conv2D(2, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(merge9)
    conv9 = Conv2D(2, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(conv9)
    conv9 = Conv2D(2, kernelsize, activation='relu', padding='same',
                   kernel_initializer='he_normal'
                   )(conv9)
    # not sure what to do with this shape
    # want to end up with 1 filter right?
    conv10 = Conv2D(1, 1, activation='sigmoid')(conv9)
    model = Model(inputs=inputs, outputs=conv10)
    model.compile(optimizer=Adam(lr=1e-3), loss='binary_crossentropy', metrics=['AUC'])

    return model

