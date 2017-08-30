import os
import time
import warnings
import numpy as np
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
import time
import matplotlib.pyplot as plt

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' #Hide messy TensorFlow warnings
warnings.filterwarnings("ignore") #Hide messy Numpy warnings
    
def load_traindata(data, seq_len, normalise_window):
    #f = open('C:/Users/Piyapong/Desktop/sp500.csv', 'rb').read()
    #data = f.decode().split('\n')

    sequence_length = seq_len + 1
    result = []
    for index in range(len(data) - sequence_length):
        result.append(data[index: index + sequence_length])
    #print (result)
    if normalise_window:
        result = normalise_windows(result)

    result = np.array(result)

    row = round(1 * result.shape[0])
    train = result[:int(row), :]
    np.random.shuffle(train)
    x_train = train[:, :-1]
    y_train = train[:, -1]


    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    return [x_train, y_train]
def gettestdata(data, normalise_window, seq_len):
    sequence_length = seq_len + 1
    result = []
    for index in range(len(data) - sequence_length + 1):
        result.append(data[index: index + sequence_length])
    if normalise_window:
        result = normalise_windows(result)

    result = np.array(result)

    row = round(0 * result.shape[0])

    x_test = result[int(row):, :-1]
    y_test = result[int(row):, -1]

    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))  

    return [x_test, y_test]
def normalise_windows(window_data):
    normalised_data = []
    for window in window_data:
        normalised_window = [((float(p) / float(window[0])) - 1) for p in window]
        normalised_data.append(normalised_window)
    return normalised_data

def denormalise_windows(d0,window_data):
    denormalised_data = []
    for p in window_data:
        denormalised_window = (float(d0) * (float(p) + 1))
        denormalised_data.append(denormalised_window)
    return denormalised_data
def build_model(layers):
    model = Sequential()

    model.add(LSTM(
        input_shape=(layers[1], layers[0]),
        output_dim=layers[1],
        return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(
        layers[2],
        return_sequences=False))
    model.add(Dropout(0.2))

    model.add(Dense(
        output_dim=layers[3]))
    model.add(Activation("linear"))

    start = time.time()
    model.compile(loss="mse", optimizer="rmsprop")
    print("> Compilation Time : ", time.time() - start)
    return model

def predict_point_by_point(model, data):
    #Predict each timestep given the last sequence of true data, in effect only predicting 1 step ahead each time
    predicted = model.predict(data)
    predicted = np.reshape(predicted, (predicted.size,))
    return predicted


def createmodel(X_train, y_train,epochs=1,seq_len=50):
    #global_start_time = time.time()
    print('> Data Loaded. Compiling...')
    model = build_model([1, seq_len, seq_len*2, 1])
    batch_size=512
    model.fit(
        X_train,
        y_train,
        batch_size=batch_size,
        nb_epoch=epochs,
        validation_split=0.05)
        
    return model

def savemodel(data,path,normalised_window,epochs=1,seq_len=50):
    """Create and save a LSTM model to a specific path.

    Parameters
    ----------
    data : 1D array_like data.
        x = np.array([1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10])
        x = df.price.values
    path : an absolute path to save a model
        path = 'C:/Users/Piyapong/Desktop/test/filename.h5'
    normalise_window: Boolean
        pre-processing data to transform the actual value to relative value (compare to the first value)
    epochs : how many times to reuse the same dataset to train a model after using all data from a previous round, optional (default = 1)
        reuse the same dataset to train a model n times. Avoid to use too many epochs to overfit a model
    seq_len : the lenght of a fragment that will be used to train a model, optional (default = 50)
        Select a length carefully to allow fragment long enough to let a model learn.

    Returns
    -------
    none : print a message 'Save model to path/to/model.h5' when the model is successfully saved.
        """
        
    x_train, y_train = load_traindata(data, seq_len, normalised_window) #fragment raw data to a training dataset
    model = createmodel(x_train, y_train,epochs,seq_len) #use the training set to train LSTM and create a model
    model.save(path)  # save the model in a HDF5 file 'my_model.h5'
    del model  # deletes the existing model
    print ('Save model to '+path)

def predicttestdata(X_test,y_test,model):
    """Load a LSTM model, use the model to predict point by point, calcualate square error between actual and predicted value by value.

    Parameters
    ----------
    X_test : 2D array_like data.
        An array of n arrays and each array contain seq_len values
    y_test : 1D array_like data.
        An array of actual values of seq_len+1 data (that we want to predict) on each segment in X_test
        You can get X_test and y_test by calling this method:
        x = np.array([1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10])
        X_test, y_test = lstmclass.gettestdata(x,50,False)

    Returns
    -------
    predictions : a 1D array of predictions point by pont from the giving set od data (X_test)
    se : a 1D array of square error between actual values and predicted values.
        caculated by (y_test - predictions) ** 2)
        Low SE = predicted values are similar to actual values ==> data follows same pattern
        High SE = predicted values are different from actual values ==> data goes in an odd pattern
        """
    scores = model.evaluate(X_test, y_test, verbose=1, batch_size=512) #evaluate the model accuracy
    print("acc : %.2f%%" % (scores*100))
    predictions = predict_point_by_point(model, X_test) #use the model to predict point by point and return an array of predictions
    se = ((y_test - predictions) ** 2) #calcualate square error
    return predictions,se
    
        
