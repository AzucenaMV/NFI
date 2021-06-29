from src.models import unet_small

# Imports
from sklearn.model_selection import train_test_split
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


