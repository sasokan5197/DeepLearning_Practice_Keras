from __future__ import print_function, division
from builtins import range
# Note: you may need to update your version of future
# sudo pip install -U future

import numpy as np
import matplotlib.pyplot as plt

from util import getKaggleMNIST
from keras.models import Model
from keras.layers import Dense, Activation, Input, BatchNormalization


# get the data
Xtrain, Ytrain, Xtest, Ytest = getKaggleMNIST()

# get shapes
N, D = Xtrain.shape
K = len(set(Ytrain))


# ANN with layers [784] -> [500] -> [300] -> [10]
i = Input(shape=(D,))
x = Dense(500)(i)
x = BatchNormalization()(x)
x = Activation('relu')(x)
x = Dense(300)(x)
x = BatchNormalization()(x)
x = Activation('relu')(x)
x = Dense(K, activation='softmax')(x)

# instantiate the model object
model = Model(inputs=i, outputs=x)

model.compile(
  loss='sparse_categorical_crossentropy',
  optimizer='adam',
  metrics=['accuracy']
)

# note: multiple ways to choose a backend
# either theano, tensorflow, or cntk


# gives us back a <keras.callbacks.History object at 0x112e61a90>
r = model.fit(Xtrain, Ytrain, validation_data=(Xtest, Ytest), epochs=15, batch_size=32)
print("Returned:", r)

# print the available keys
# should see: dict_keys(['val_loss', 'acc', 'loss', 'val_acc'])
print(r.history.keys())

# plot some data
plt.plot(r.history['loss'], label='loss')
plt.plot(r.history['val_loss'], label='val_loss')
plt.legend()
plt.show()

# accuracies
plt.plot(r.history['acc'], label='acc')
plt.plot(r.history['val_acc'], label='val_acc')
plt.legend()
plt.show()


# make predictions and evaluate
probs = model.predict(Xtest) # N x K matrix of probabilities
Ptest = np.argmax(probs, axis=1)
print("Validation acc:", np.mean(Ptest == Ytest))

