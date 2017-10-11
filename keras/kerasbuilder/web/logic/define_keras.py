#!encoding=utf-8



LAYER = [
    {
        "name":"Dense",
        "module":"keras.layers.core.Dense",
        "comments":""" 
                        implements the operation: output = activation(dot(input, kernel) + bias) where activation is the element-wise activation function passed as the activation argument, kernel is a weights matrix created by the layer, and bias is a bias vector created by the layer (only applicable if use_bias is True).
                        """,
        "params":[
            {
                "name":"units",
                "comments":"Positive integer, dimensionality of the output space",
                "regex":"n",
                "default":1,
                "pt":1,
                "dt":'int'
            },
            {
                "name":"activation",
                "comments":"Activation function to use (see activations). If you don't specify anything, no activation is applied (ie. 'linear' activation: a(x) = x).",
                "regex":"",
                "default":'input number',
            },
            {
                "name":'input_dim',
                "dt":'int'
            }
        ]
    },
    {
        "name":"Activation",
        "module":"keras.layers.core.Activatio",
        "comments":"""Applies an activation function to an output.""",
        "params":[
            {
                "name":"activation",
                "comments":"name of activation function to use (see: activations), or alternatively, a Theano or TensorFlow operation.",
                "regex":"s",
                "default":None,
                "pt":1,
                "dt":'str'
            },
        ]
    },
    {
        "name":"Dropout",
        "module":"keras.layers.core.Dropout",
        "comments":"""Applies Dropout to the input.
                    Dropout consists in randomly setting a fraction rate of input units to 0 at each update during training time, which helps prevent overfitting.""",
        "params":[
            {
                "name":"rate",
                "comments":"float between 0 and 1. Fraction of the input units to drop.",
                "regex":"/^[0-9]\d*\.\d*|0\.\d*[0-9]\d*$/",
                "default":None,
                "dt":'float',
                "pt":1
            },
            {
                "name":"noise_shape",
                "comments":" 1D integer tensor representing the shape of the binary dropout mask that will be multiplied with the input. For instance, if your inputs have shape  (batch_size, timesteps, features) and you want the dropout mask to be the same for all timesteps, you can use noise_shape=(batch_size, 1, features)",
                "regex":"",
                "default":None,
            },
            {
                "name":"seed",
                "comments":"A Python integer to use as random seed",
                "regex":"",
                "default":None,
            },
        ]
    },
    {
        "name":"Flatten",
        "module":"keras.layers.core.Flatten",
        "comments":"""Flattens the input. Does not affect the batch size.""",
    },
    {
        "name":"Reshape",
        "module":"keras.layers.core.Reshape",
        "comments":"""Reshapes an output to a certain shape.""",
        "params":[
            {
                "name":"target_shape",
                "comments":"target shape. Tuple of integers, does not include the samples dimension (batch size).",
                "regex":"",
                "default":"",
            },
        ]
    },
    {
        "name":"Permute",
        "module":"keras.layers.core.Permute",
        "comments":"""Permutes the dimensions of the input according to a given pattern.
                                    Useful for e.g. connecting RNNs and convnets together.""",
        "params":[
            {
                "name":"dims",
                "comments":"Tuple of integers. Permutation pattern, does not include the samples dimension. Indexing starts at 1. For instance, (2, 1) permutes the first and second dimension of the input",
                "regex":"/^\(\d+,{1}\d+\)+/",
                "default":"",
            },
        ]
    },
    {
        "name":"RepeatVector",
        "module":"keras.layers.core.RepeatVector",
        "comments":"""Repeats the input n times.""",
        "params":[
            {
                "name":"n",
                "comments":"integer, repetition factor.",
                "regex":"n",
                "default":"",
                "pt":1,
                "dt":'int'
            },
        ]
    },
    {
        "name":"Lambda",
        "module":"keras.layers.core.Lambda",
        "comments":"""Wraps arbitrary expression as a Layer object.""",
        "params":[
            {
                "name":"function",
                "comments":"The function to be evaluated. Takes input tensor as first argument.",
                "regex":"*",
                "default":None,
                "pt":1,
            },
            {
                "name":"output_shape",
                "comments":"Expected output shape from function",
                "regex":"",
                "default":None,
            },
            {
                "name":"mask",
                "comments":"The function to be evaluated. Takes input tensor as first argument.",
                "regex":"",
                "default":None,
            },
            {
                "name":"arguments",
                "comments":"optional dictionary of keyword arguments to be passed to the function.",
                "regex":"",
                "default":None,
            },
        ]
    },
    {
        "name":"ActivityRegularization",
        "module":"keras.layers.core.ActivityRegularization",
        "comments":"""Layer that applies an update to the cost function based input activity.""",
        "params":[
            {
                "name":"l1",
                "comments":" L1 regularization factor (positive float).",
                "regex":"/^[0-9]\d*\.\d*|0\.\d*[0-9]\d*$/",
                "default":"",
                "pt":1,
                "dt":'float'
            },
            {
                "name":"l2",
                "comments":" L2 regularization factor (positive float).",
                "regex":"/^[0-9]\d*\.\d*|0\.\d*[0-9]\d*$/",
                "default":"",
                "pt":1,
                "dt":'float'
            },
        ]
    },
    {
        "name":"Masking",
        "module":"keras.layers.core.Masking",
        "comments":"""Masks a sequence by using a mask value to skip timesteps.""",
        "params":[
            {
                "name":"mask_value",
                "comments":"",
                "regex":"/^[0-9]\d*\.\d*|0\.\d*[0-9]\d*$/",
                "default":0.0,
                "pt":1,
                "dt":'float'
            },
        ]
    },
]


OPTIMIZER = [
    {
        "name":"SGD",
        "module":"keras.optimizers.SGD",
        "comments":"""Stochastic gradient descent optimizer.
                            Includes support for momentum, learning rate decay, and Nesterov momentum.""",
        "params":[
            {
                "name":"lr",
                "comments":" float >= 0. Learning rate.",
                "regex":"/^[0-9]\d*\.\d*|0\.\d*[0-9]\d*$/",
                "default":0.01,
                "dt":'float'
            },
            {
                "name":"momentum",
                "comments":" float >= 0. Parameter updates momentum.",
                "regex":"/^[0-9]\d*\.\d*|0\.\d*[0-9]\d*$/",
                "default":0.0,
                "dt":'float'
            },
            {
                "name":"decay",
                "comments":"float >= 0. Learning rate decay over each update.",
                "regex":"/^[0-9]\d*\.\d*|0\.\d*[0-9]\d*$/",
                "default":0.0,
                "dt":'float'
            },
            {
                "name":"nesterov",
                "comments":"boolean. Whether to apply Nesterov momentum.",
                "regex":"",
                "default":False,
                "dt":'bool',
            },
        ]
    },
    {
        "name":"RMSprop",
        "module":"keras.optimizers.RMSprop",
        "comments":
            """
                It is recommended to leave the parameters of this optimizer at their default values (except the learning rate, which can be freely tuned).
                This optimizer is usually a good choice for recurrent neural networks.
            """,
        "params":[
            {
                "name":"lr",
                "comments":"float >= 0. Learning rate.",
                "regex":"/^[0-9]\d*\.\d*|0\.\d*[0-9]\d*$/",
                "default":0.01,
                "dt":'float'
            },
            {
                "name":"rho",
                "comments":" float >= 0.",
                "regex":"/^[0-9]\d*\.\d*|0\.\d*[0-9]\d*$/",
                "default":0.9,
                "dt":'float'
            },
            {
                "name":"epsilon",
                "comments":"float >= 0. Fuzz factor.",
                "regex":"",
                "default":1e-08,
                "dt":'float'
            },
            {
                "name":"decay",
                "comments":"float >= 0. Learning rate decay over each update.",
                "regex":"/^[0-9]\d*\.\d*|0\.\d*[0-9]\d*$/",
                "default":0.0,
                "dt":'float'
            },
        ]
    },
    {
        "name":"Adagrad",
        "module":"keras.optimizers.Adagrad",
        "comments":
            """
                It is recommended to leave the parameters of this optimizer at their default values.
            """,
        "params":[
            {
                "name":"lr",
                "comments":"float >= 0. Learning rate.",
                "regex":"/^[0-9]\d*\.\d*|0\.\d*[0-9]\d*$/",
                "default":0.01,
                "dt":'float'
            },

            {
                "name":"epsilon",
                "comments":"float >= 0. Fuzz factor.",
                "regex":"",
                "default":1e-08,
                "dt":'float'
            },
            {
                "name":"decay",
                "comments":"float >= 0. Learning rate decay over each update.",
                "regex":"/^[0-9]\d*\.\d*|0\.\d*[0-9]\d*$/",
                "default":0.0,
                "dt":'float'
            },
        ]
    },
    {
        "name":"Adadelta",
        "module":"keras.optimizers.Adadelta",
        "comments":
            """
            It is recommended to leave the parameters of this optimizer at their default values.
            """,
        "params":[
            {
                "name":"lr",
                "comments":"float >= 0. Learning rate.",
                "regex":"/^[0-9]\d*\.\d*|0\.\d*[0-9]\d*$/",
                "default":0.01,
                "dt":'float'
            },
            {
                "name":"rho",
                "comments":" float >= 0.",
                "regex":"/^[0-9]\d*\.\d*|0\.\d*[0-9]\d*$/",
                "default":0.95,
                "dt":'float'
            },
            {
                "name":"epsilon",
                "comments":"float >= 0. Fuzz factor.",
                "regex":"",
                "default":1e-08,
                "dt":'float'
            },
            {
                "name":"decay",
                "comments":"float >= 0. Learning rate decay over each update.",
                "regex":"/^[0-9]\d*\.\d*|0\.\d*[0-9]\d*$/",
                "default":0.0,
                "dt":'float'
            },
        ]
    },
    {
        "name":"Adam",
        "module":"keras.optimizers.Adam",
        "comments":
            """
            Default parameters follow those provided in the original paper.
            """,
        "params":[
            {
                "name":"lr",
                "comments":"float >= 0. Learning rate.",
                "regex":"/^[0-9]\d*\.\d*|0\.\d*[0-9]\d*$/",
                "default":0.001,
                "dt":'float'
            },
            {
                "name":"beta_1",
                "comments":" float, 0 < beta < 1. Generally close to 1.",
                "regex":"/^[0-9]\d*\.\d*|0\.\d*[0-9]\d*$/",
                "default":0.9,
                "dt":'float'
            },
            {
                "name":"beta_2",
                "comments":"float, 0 < beta < 1. Generally close to 1.",
                "regex":"/^[0-9]\d*\.\d*|0\.\d*[0-9]\d*$/",
                "default":0.999,
                "dt":'float'
            },
            {
                "name":"epsilon",
                "comments":"float >= 0. Fuzz factor.",
                "regex":"",
                "default":1e-08,
                "dt":'float'
            },
            {
                "name":"decay",
                "comments":"float >= 0. Learning rate decay over each update.",
                "regex":"/^[0-9]\d*\.\d*|0\.\d*[0-9]\d*$/",
                "default":0.0,
                "dt":'float'
            },
        ]
    },
    {
        "name":"Adamax",
        "module":"keras.optimizers.Adamax",
        "comments":
            """
            It is a variant of Adam based on the infinity norm. Default parameters follow those provided in the paper.
            """,
        "params":[
            {
                "name":"lr",
                "comments":"float >= 0. Learning rate.",
                "regex":"/^[0-9]\d*\.\d*|0\.\d*[0-9]\d*$/",
                "default":0.002,
            },
            {
                "name":"beta_1",
                "comments":" float, 0 < beta < 1. Generally close to 1.",
                "regex":"/^[0-9]\d*\.\d*|0\.\d*[0-9]\d*$/",
                "default":0.9,
            },
            {
                "name":"beta_2",
                "comments":"float, 0 < beta < 1. Generally close to 1.",
                "regex":"/^[0-9]\d*\.\d*|0\.\d*[0-9]\d*$/",
                "default":0.999,
            },
            {
                "name":"epsilon",
                "comments":"float >= 0. Fuzz factor.",
                "regex":"",
                "default":1e-08,
            },
            {
                "name":"decay",
                "comments":"float >= 0. Learning rate decay over each update.",
                "regex":"/^[0-9]\d*\.\d*|0\.\d*[0-9]\d*$/",
                "default":0.0,
            },
        ]
    },
    {
        "name":"Nadam",
        "module":"keras.optimizers.Nadam",
        "comments":
            """
            Much like Adam is essentially RMSprop with momentum, Nadam is Adam RMSprop with Nesterov momentum.

            Default parameters follow those provided in the paper. It is recommended to leave the parameters of this optimizer at their default values.
            """,
        "params":[
            {
                "name":"lr",
                "comments":"float >= 0. Learning rate.",
                "regex":"/^[0-9]\d*\.\d*|0\.\d*[0-9]\d*$/",
                "default":0.002,
            },
            {
                "name":"beta_1",
                "comments":" float, 0 < beta < 1. Generally close to 1.",
                "regex":"/^[0-9]\d*\.\d*|0\.\d*[0-9]\d*$/",
                "default":0.9,
            },
            {
                "name":"beta_2",
                "comments":"float, 0 < beta < 1. Generally close to 1.",
                "regex":"/^[0-9]\d*\.\d*|0\.\d*[0-9]\d*$/",
                "default":0.999,
            },
            {
                "name":"epsilon",
                "comments":"float >= 0. Fuzz factor.",
                "regex":"",
                "default":1e-08,
            },
            {
                "name":"schedule_decay",
                "comments":"",
                "regex":"/^[0-9]\d*\.\d*|0\.\d*[0-9]\d*$/",
                "default":0.004,
            },
        ]
    },
]
LOSSES = [
    "mean_squared_error",
    "mean_absolute_error",
    "mean_absolute_percentage_error",
    "mean_squared_logarithmic_error",
    "squared_hinge",
    "hinge",
    "logcosh",
    "categorical_crossentropy",
    "sparse_categorical_crossentropy",
    "binary_crossentropy",
    "kullback_leibler_divergence",
    "poisson",
    "cosine_proximity",
]

METRICS = [
 'binary_accuracy',
 'binary_crossentropy',
 'categorical_accuracy',
 'categorical_crossentropy',
 'cosine',
 'cosine_proximity',
 'f1score',
 'fbeta_score',
 'fmeasure',
 'fscore',
 'hinge',
 'kullback_leibler_divergence',
 'mae',
 'mape',
 'matthews_correlation',
 'mean_absolute_error',
 'mean_absolute_percentage_error',
 'mean_squared_error',
 'mean_squared_logarithmic_error',
 'mse',
 'msle',
 'poisson',
 'precision',
 'sparse_categorical_accuracy',
 'sparse_categorical_crossentropy',
 'squared_hinge',
 'top_k_categorical_accuracy']
