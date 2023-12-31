import os
import random
import numpy as np
from keras.src.utils import to_categorical

from tensorflow.python.ops.batch_ops import batch

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow import keras
from keras import layers, regularizers

from solution import numbers, getAnswerFirst, getAnswerSecond

def defineModelOriginal():
    # max accuracy 0.5522, 0.4390
    input_length = 57  # Length of your input sequences
    embedding_dim = 50  # Dimension of the embedding space
    lstm_units = 64  # Number of units in the LSTM layer
    
    inputs = tf.keras.Input(shape=(1,input_length))
    #x = layers.Embedding(input_dim=37, output_dim=100, input_length=57)(inputs)
    #x = layers.Conv1D(64, 3, activation='relu')(x)
    x = layers.LSTM(512, return_sequences=True, activation='relu')(inputs)
    x = layers.LSTM(512, activation='relu')(x)
    x = layers.Dense(512, activation='relu')(x)
    x = layers.Dropout(0.1)(x)
    output1 = layers.Dense(10, activation='softmax', name='first_num')(x)
    output2 = layers.Dense(10, activation='softmax', name='second_num')(x)
    
    model = keras.Model(inputs = inputs, outputs=[output1, output2])

    model.compile(loss='sparse_categorical_crossentropy', optimizer=keras.optimizers.Adam(learning_rate=0.001),  metrics=['accuracy'])

    return model

def defineModelRNN():
    # max accuracy 0.5522, 0.4390
    input_length = 57  # Length of your input sequences
    embedding_dim = 50  # Dimension of the embedding space
    lstm_units = 64  # Number of units in the LSTM layer

    model = tf.keras.models.Sequential()
    #model.add(layers.Embedding(input_dim=37, output_dim=100, input_length=57))
    model.add(keras.Input(shape=(1,57)))
    model.add(layers.SimpleRNN(512, return_sequences=True, activation='relu'))
    model.add(layers.SimpleRNN(512, activation='relu'))
    model.add(layers.Dense(512, activation='relu'))
    model.add(layers.Dropout(0.1))
    model.add(layers.Dense(10, activation='softmax'))

    model.compile(loss='sparse_categorical_crossentropy', optimizer=keras.optimizers.Adam(learning_rate=0.001),  metrics=['accuracy'])

    return model

def defineModelGRU():
    # max accuracy 0.5575, 0.4400
    input_length = 57  # Length of your input sequences
    embedding_dim = 50  # Dimension of the embedding space
    lstm_units = 64  # Number of units in the LSTM layer

    model = tf.keras.models.Sequential()
    #model.add(layers.Embedding(input_dim=37, output_dim=100, input_length=57))
    model.add(keras.Input(shape=(1,57)))
    model.add(layers.GRU(512, return_sequences=True, activation='relu'))
    model.add(layers.GRU(512, activation='relu'))
    #model.add(layers.Dense(512, activation='relu'))
    #model.add(layers.Dropout(0.1))
    model.add(layers.Dense(10, activation='softmax'))

    model.compile(loss='sparse_categorical_crossentropy', optimizer=keras.optimizers.Adam(learning_rate=0.001),  metrics=['accuracy'])

    return model


def defineModelLSTM():
    # max accuracy 0.5709, 0.4310
    input_length = 57  # Length of your input sequences
    embedding_dim = 50  # Dimension of the embedding space
    lstm_units = 64  # Number of units in the LSTM layer

    model = tf.keras.models.Sequential()
    #model.add(layers.Embedding(input_dim=37, output_dim=100, input_length=57))
    model.add(keras.Input(shape=(1,57)))
    model.add(layers.LSTM(512, return_sequences=True, activation='relu'))
    model.add(layers.LSTM(512, activation='relu'))
    #model.add(layers.Dense(512, activation='relu'))
    #model.add(layers.Dropout(0.1))
    model.add(layers.Dense(10, activation='softmax'))

    model.compile(loss='sparse_categorical_crossentropy', optimizer=keras.optimizers.Adam(learning_rate=0.001),  metrics=['accuracy'])

    return model


def defineModelLSTMBidirect():
    # max accuracy 0.5575, 0.4400
    input_length = 57  # Length of your input sequences
    embedding_dim = 50  # Dimension of the embedding space
    lstm_units = 64  # Number of units in the LSTM layer

    model = tf.keras.models.Sequential()
    #model.add(layers.Embedding(input_dim=37, output_dim=100, input_length=57))
    model.add(keras.Input(shape=(1,57)))
    model.add(layers.Bidirectional(layers.LSTM(512, return_sequences=True, activation='relu')))
    model.add(layers.Bidirectional(layers.LSTM(512, return_sequences=True, activation='relu')))
    #model.add(layers.Dense(512, activation='relu'))
    #model.add(layers.Dropout(0.1))
    model.add(layers.Dense(10, activation='softmax'))
    model.compile(
        loss={
            'first_num': 'sparse_categorical_crossentropy',
            'second_num': 'sparse_categorical_crossentropy'
        },
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        metrics={
            'first_num': 'accuracy',
            'second_num': 'accuracy'
        }
    )


    return model

defineModel = defineModelOriginal

def generateTrainingData(count):
    for i in range(count):
        result = ""
        l = random.randint(3, 57)
        for j in range(l):
            c = random.randint(0, 45)
            if c < 26:
                result += chr(c + ord('a'))
            
            elif c < 36:
                result += chr(c - 26 + ord('0'))
                
            else:
                result += numbers[c-36]
        
        for j in range(2):
            loc = random.randint(0, l-1)
            result = result[:loc] + str(random.randint(0, 9)) + result[loc:]
        
        result = result[:l]
        yield result


def convertToModelInput(value, l):
    result = []
    for i in range(l):
        c = '\0'
        if i < len(value):
            c = value[i].lower()
        if c >= '0' and c <= '9':
            result.append(0 + int(c) + 1)
        elif c >= 'a' and c <= 'z':
            result.append(10 + ord(c) - ord('a') + 1)
        elif c == '\0':
            result.append(0)
        else:
            assert(False)

    return result

def getTrainingData(count):
    x_source = [x for x in generateTrainingData(count)]
    
    x_train = np.array([convertToModelInput(x, 57) for x in x_source])
    x_train = np.reshape(x_train, (-1, 1, 57))
    
    result = [getAnswerFirst(x) for x in x_source]
    y_train_first = np.array([x[0] for x in result])
    y_train_second = np.array([x[1] for x in result])
    
    return (x_source, x_train, y_train_first, y_train_second)

def getTestData():
    from solution import inp as x_source
    x_train = np.array([convertToModelInput(x, 57) for x in x_source])
    
    x_train = np.reshape(x_train, (-1, 1, 57))
    
    result = [getAnswerFirst(x) for x in x_source]
    y_train_first = np.array([x[0] for x in result])
    y_train_second = np.array([x[1] for x in result])
    
    return (x_source, x_train, y_train_first, y_train_second)

model = defineModel()
print(model.summary())


(source, x_train, y_train_first, y_train_second) = getTrainingData(100000)

for i in range(10):
    print(f"{source[i]} - {x_train[0]} - {y_train_first[i]} - {y_train_second[i]}")

model.fit(x_train, [y_train_first, y_train_second], epochs=250, batch_size=64, verbose=2)

(_, x_test, y_train_first, y_train_second) = getTestData()
model.save("model.h5")
model.evaluate(x_test, [y_train_first, y_train_second], batch_size=64, verbose=2)