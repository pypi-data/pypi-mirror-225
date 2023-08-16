import numpy as np, tensorflow as tf, warnings, os
from tensorflow.keras.layers import (LSTM, BatchNormalization, Dense, Input, LeakyReLU)
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam, SGD
from tensorflow.keras.regularizers import l2

warnings.filterwarnings('ignore')  # remove TF clutter
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}


def train_lstm(x, y, d_params):
    """ Creates a model and fits it with the given data and configuration."""

    h_params = {**d_params["h_params"], **d_params["timeseries"]["lstm"]}

    layers = [Input((x.shape[1:]), name='input_lstm_0')]
    layers += [model_lstm_layers(h_params, layers[0])]
    layers += [model_final_layer(layers[-1], y, h_params)]
    model = Model(inputs=layers[0], outputs=layers[-1])

    # TODO: we cast the learning rate to float in learntime, but not in explain. 
    # saved as float casting here, but note it might cause problems! 
    optimizer = {
        'adam': Adam(learning_rate=float(h_params['learning_rate'])),
        'sgd': SGD(learning_rate=float(h_params['learning_rate'])),
    }

    model.compile(
        optimizer=optimizer[h_params['optimizer']],
        loss=d_params['metrics'][0], 
        metrics=d_params['metrics']
    )

    # TODO: model checkpoint correct? 
    if ('train_local' in h_params) and (h_params['train_local'] is not None): 
        checkpoint_path = h_params['train_local']['checkpoint_path']
        callbacks = [tf.keras.callbacks.ModelCheckpoint(f'{checkpoint_path}/{d_params["mid"]}/{d_params["hid"]}/model.h5', save_best_only=True, save_freq='epoch', verbose=1)]
    else: 
        callbacks = [tf.keras.callbacks.ModelCheckpoint(f'/mnt/models/{d_params["mid"]}/{d_params["hid"]}/model.h5', save_best_only=True, save_freq='epoch', verbose=1)]
    # TODO: in explain tab time, we have this set to just *.h5, not model.h5. considering this is the training loop the current code (model.h5) from learn-time should be correct. 
    # callbacks = [tf.keras.callbacks.ModelCheckpoint(f'/mnt/models/{d_params["mid"]}/{d_params["hid"]}.h5', save_best_only=True, save_freq='epoch', verbose=1)]

    if ('train_local' not in h_params) or (not h_params['train_local']):
        callbacks += [
            tf.keras.callbacks.RemoteMonitor(
                root=d_params["url"],
                path=f'/api/v1/add-learn-log/{d_params["mid"]}/{d_params["hid"]}',
                send_as_json=True
            )
        ]

    history = model.fit(x=x, y=y, batch_size=h_params['batch_size'], epochs=h_params['epochs'],
                             callbacks=callbacks, validation_split=0.3)

    return history, model


def model_lstm_layers(h_params, input_layer_0):

    flag_lstm_layer = False

    for i in range(h_params["LSTM_layers"]):
        return_sequences = True if h_params.get(
            'use_attention') else i < (h_params['LSTM_layers']-1)

        if i > 0:
            flag_lstm_layer = True
        act_to_use = h_params['activation'] if i != 0 else h_params['first_activation']

        # and not lag_lstm_layer:
        if h_params['LSTM_batch_norm'] and act_to_use not in ['sigmoid', 'tanh']:
            lstm_layer = BatchNormalization()(lstm_layer if flag_lstm_layer else input_layer_0)

        if act_to_use != "lrelu":
            if h_params['l1_l2'] != 0:
                lstm_layer = LSTM(units=h_params['LSTM_nodes'], activation=act_to_use, return_sequences=return_sequences, kernel_regularizer=l2(h_params['l1_l2']), recurrent_regularizer=l2(h_params['l1_l2']), bias_regularizer=l2(h_params['l1_l2'])
                                  )(lstm_layer if flag_lstm_layer else input_layer_0)
            else:
                lstm_layer = LSTM(units=h_params['LSTM_nodes'], activation=act_to_use, return_sequences=return_sequences)(
                    lstm_layer if flag_lstm_layer else input_layer_0)
        elif h_params['l1_l2'] != 0:
            lstm_layer = LSTM(units=h_params['LSTM_nodes'],
                              return_sequences=return_sequences,
                              kernel_regularizer=l2(0.01), recurrent_regularizer=l2(0.01), bias_regularizer=l2(0.01)
                              )(lstm_layer if flag_lstm_layer else input_layer_0)
        else:
            lstm_layer = LSTM(units=h_params['LSTM_nodes'], return_sequences=return_sequences)(
                lstm_layer if flag_lstm_layer else input_layer_0)

        if act_to_use == 'lrelu':
            lstm_layer = LeakyReLU()(lstm_layer)

        if h_params['LSTM_batch_norm'] and act_to_use in ['sigmoid', 'tanh']:
            lstm_layer = BatchNormalization()(lstm_layer)

    if h_params['LSTM_batch_norm'] and act_to_use not in ['sigmoid', 'tanh']:
        lstm_layer = BatchNormalization()(lstm_layer)

    return lstm_layer

def model_final_layer(final_layer, y, h_params):


    if h_params['final_activation'] != 'lrelu':
        final_layer = Dense(
            y.shape[-1], activation=h_params['final_activation'])(final_layer)
    else:
        final_layer = Dense(y.shape[-1])(final_layer)
        final_layer = LeakyReLU()(final_layer)
    return final_layer
