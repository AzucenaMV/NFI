import tensorflow as tf
from src.classes import *
from src.models import dense_model, unet_from_aml, unet_small, unet_tiny, model_for_example
import matplotlib.pyplot as plt

# Imports
from sklearn.datasets import make_multilabel_classification
from sklearn.model_selection import train_test_split
from tensorflow.keras.losses import binary_crossentropy
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard, LearningRateScheduler


def unet(train_input, length, weights = 'data/weights_norm_avgpool.h5', train = True):
    """unet training. Default is training and storing under weights.h5"""
    number_of_dyes = 6
    model = unet_small((length, number_of_dyes, 1))
    model.summary()
    model.load_weights(weights)

    if train:
        all_images = train_input.data
        all_labels = train_input.labels
        train_images, test_images, train_labels, test_labels = train_test_split(all_images, all_labels, test_size=0.5, random_state=42)
        batch_size = 10  # number of samples processed before the model is updated
        num_epochs = 10  # number of complete passes through the training dataset before the training stops
        model_checkpoint = ModelCheckpoint(weights, monitor='val_loss', save_best_only=True)
        # tensorboard_callback = TensorBoard(log_dir="./logs")
        # def scheduler(epoch, lr):
        #     if epoch < 10:
        #         return lr
        #     else:
        #         return lr * tf.math.exp(-0.1)
        # scheduler_callback = LearningRateScheduler(scheduler)
        # history is optional for plotting
        history = model.fit(train_images, train_labels, batch_size=batch_size, epochs=num_epochs, verbose=1, shuffle=True,
                        validation_split=0.2, callbacks=[model_checkpoint])
        metric_values = model.evaluate(x=test_images, y=test_labels)
        print('Final TEST performance')
        for metric_value, metric_name in zip(metric_values, model.metrics_names):
            print('{}: {}'.format(metric_name, metric_value))

    return model


def simplest_nn(train_input: OldTrainInput):
    number_of_dyes = 5
    # TODO: maybe use np.tile to get same data multiple times
    all_images = train_input.data
    print(all_images.shape)
    #all_images = all_images.reshape(-1, width, number_of_dyes, 1)
    all_labels = train_input.labels
    print(all_labels.shape)
    train_images, test_images, train_labels, test_labels = train_test_split(all_images, all_labels, test_size=0.33, random_state=42)

    model = dense_model(number_of_dyes)
    # model.summary()
    batch_size = 50  # number of samples processed before the model is updated
    num_epochs = 10  # number of complete passes through the training dataset before the training stops

    # Compiling the model adds a loss function, optimiser and metrics to track during training
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.01),
                  loss=tf.keras.losses.BinaryCrossentropy(),
                  metrics=['accuracy', 'AUC'])
    # history is optional for plotting
    history = model.fit(x=train_images,
              y=train_labels,
              batch_size=batch_size,
              epochs=num_epochs,
              validation_split = 0.33)


    metric_values = model.evaluate(x=test_images, y=test_labels)
    print('Final TEST performance')
    for metric_value, metric_name in zip(metric_values, model.metrics_names):
        print('{}: {}'.format(metric_name, metric_value))

    # for row in all_images:
    #     print(model.predict(row.reshape(1,161,5)))
    return model

