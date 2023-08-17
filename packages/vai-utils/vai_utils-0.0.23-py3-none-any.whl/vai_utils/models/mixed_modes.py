#!/usr/bin/env python
# coding: utf-8
################################################################################
"""
NEURAL NETWORK CLASS MODULE

pretrained_glove: load embedding from pretrained glove
custom_standardization: layers preprocessing for text data
text_prep_layer: text preprocessing layer
normalize_layer: normalize data layer, 0-255
image_prep_layer: image preprocessing layer
rnn_layer: RNN layer
deep_layer: DNN layer


The ideal machine learning model is end-to-end
The ideal model should expect as input something as close as possible to raw data:
and a text model should accept strings of utf-8 characters

"""
################################################################################

import tensorflow as tf
import tensorflow as text  # need to keep this line to work
# from text import bert
#import neural_structured_learning as nsl # TODO ?

class NETWORK(tf.keras.Model):
    def __init__(self, X, Y, d_params, h_params):
        super(NETWORK, self).__init__()

        #if "GPU" not in str(tf.config.list_physical_devices()):  # TODO: check for gpu on GPU compati.
        #    raise Exception("Error: GPU not being used")

        self.columns = X.columns
        self.F, self.O = 0, Y.shape[-1]

        """ INPUT LAYER """
        self.dtypes_x = {k: val["type"] for k, val in d_params["x"].items()}
        self.dtypes_y = {k: val["type"] for k, val in d_params["y"].items()}
        self.dtypes = list(zip(X.dtypes.index, X.dtypes))  # get dtypes

        # Use Dtypes to Create Mixed Data
        input_els, encoded_els = [], []
        for k, dtype in self.dtypes_x.items():  # structure the data
            self.F += 1
            if dtype == "CATEGORY":  # categorical data (str, int, bool)
                input_els.append(tf.keras.Input(shape=(1,), dtype=tf.int32))
                n = len(X[k].unique())
                x = tf.keras.layers.Embedding(n+1, 1)(input_els[-1])  # takes only 999 size
                e = tf.keras.layers.Flatten()(x)
                self.F += n
            elif dtype == "NUMBER":  # continuous data (float, int)
                input_els.append(tf.keras.Input(shape=(1,), dtype=tf.float32))
                e = tf.keras.layers.BatchNormalization()(input_els[-1])  # TODO verify int cont. works like this
            elif dtype == "STRING":  # textual data (str)
                input_els.append(tf.keras.Input(shape=(1,), dtype=tf.string))
                # encoder = bert.NETWORK(h_params, Y.shape[-1])
                e = encoder(input_els[-1])
            #elif dtype == "STRUCTURED":  # TODO: pass structured as var or
            #    #graph_config = nsl.configs.GraphRegConfig(neighbor_config=nsl.configs.GraphNeighborConfig(max_neighbors=1)) 
            #    #graph_model = nsl.keras.GraphRegularization(base_model, graph_config)
            #    
            else:
                raise Exception(dtype)
            encoded_els.append(e)

        x = tf.keras.layers.concatenate(encoded_els)  # layers are now merged

        # Deep Layer
        n = x.shape.as_list()[-1]
        for i in range(h_params["deep_lyrs"]):
            x = tf.keras.layers.Dense(n, activation="relu")(x)

        # Add Regularization For Small Datasets
        # x = tf.keras.layers.Dropout(0.5)(x)

        """ TRANSLATION LAYER """

        # Output Layer TODO different activations
        out = tf.keras.layers.Dense(self.O, activation="sigmoid")(x)

        self.model = tf.keras.Model(inputs=input_els, outputs=[out])

        """ LOSS """

        # Check if Binary  TODO multiple types of output & cost
        binary = len(list(set(Y.values.ravel('K')))) == 2

        if binary and (self.O == 1):  # binary
            self.loss, self.metric = "binary_crossentropy", [tf.keras.metrics.BinaryAccuracy()]
        elif binary and (self.O > 1):  # binary
            self.loss, self.metric = "categorical_crossentropy", [tf.keras.metrics.CategoricalAccuracy()]
        elif not binary:
            self.loss, self.metric = "mse", [tf.keras.metrics.MeanSquaredError()]
        else:
            raise Exception("Error: loss not setup in network.py")

    # @tf.function  # (input_signature=(tf.TensorSpec(shape=(None, 12), dtype=tf.float32),))
    # def f(self, X):
    #     return self.model(tf.unstack(tf.transpose(X)))

    def call(self, x, training=False):
        if training:
            return self.model(x)
        else:
            try:
                print("eagerly == false", x.numpy())
            except:
                pass
            return self.model(x)


    #def get_config(self):
    #    return {"hidden_units": self.hidden_units}
    #
    #@classmethod
    #def from_config(cls, config):
    #    return cls(**config)
