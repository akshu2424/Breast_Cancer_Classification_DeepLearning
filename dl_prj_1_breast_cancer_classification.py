# -*- coding: utf-8 -*-
"""DL prj 1.Breast Cancer Classification.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QY0TKAVByR6U48OWJT86-ad0N8INXXku

# **Breast Cancer Classification with a  Neural Network (NN)**
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn.datasets
from sklearn.model_selection import train_test_split

"""Data Collection and processing"""

# loading the data from sklearn
breast_cancer_dataset = sklearn.datasets.load_breast_cancer()

print(breast_cancer_dataset)

# loading the data to a data frame
data_frame = pd.DataFrame(breast_cancer_dataset.data, columns = breast_cancer_dataset.feature_names)

data_frame.head()

#adding target column to the data frame
data_frame['label']=breast_cancer_dataset.target

data_frame.tail()

data_frame.shape

data_frame.info()

data_frame.isnull().sum()

# statistical measures
data_frame.describe()

data_frame['label'].value_counts()

"""1 - benign

0 - malignant
"""

data_frame.groupby('label').mean()

"""separating features and target"""

X = data_frame.drop(columns=['label'],axis=1)
Y = data_frame['label']

"""Splitting data into training and testing data"""

X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.2,random_state=2)

"""#Standardize the data
if we use standardize data then in model building loss decreases and accuracy increase while we use our normal trainning data and test data it will not give more accuracy and increases loss

"""

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_std = scaler.fit_transform(X_train)
X_test_std = scaler.transform(X_test)

"""# Building the Neural Network"""

# importing tensorflow and Keras
import tensorflow as tf
tf.random.set_seed(3) # you're essentially fixing the random number generator to produce the same sequence of random numbers every time the code is run
#so this  will ensure your output will be the same as it set some intial operation
from tensorflow import keras

# setting the layers of the Neural network
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(30,)),
    keras.layers.Dense(20,activation='relu'),#20 = no. neurons in the layer
    keras.layers.Dense(2,activation='sigmoid') # o.p layer contain 2 neurons
])

# coompiling the Neural network
#compile method used to configure model for training
model.compile(
    optimizer ='adam', #optimization algorithm used to update the weights of the neural network during training
    loss='sparse_categorical_crossentropy',
#above loss= a loss function used in classification problems where the target labels are integers (e.g., 0, 1, 2) and not one-hot encoded
    metrics=['accuracy']
#metrics: Specifies the evaluation metrics used to monitor the performance of the model during training and testing. Here, 'accuracy' is used to measure the classification accuracy of the model.
)

#trainning the neural network
history =model.fit(X_train_std,Y_train,validation_split=0.1,epochs=10)
#model.fit: Method to train the neural network on the provided dataset.
#X_train_std: Input data for training (standardized).
#Y_train: Target labels corresponding to the input data.
#validation_split: Fraction of the training data used for validation during training to avoid overfitting.
#epochs: Number of times the entire dataset is fed to the neural network for training.

"""Visualizing accuracy and loss"""

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])

plt.title('model_accuracy')
plt.xlabel('epoch')
plt.ylabel('accuracy')

plt.legend(['training data','validation data'],loc ='lower right')

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])

plt.title('model loss')
plt.xlabel('epoch')
plt.ylabel('loss')

plt.legend(['training data','validation data'],loc='upper right')

"""Accuracy of the model on test data"""

loss , accuracy = model.evaluate(X_test_std,Y_test)
print(accuracy)
print(loss)

print(X_test_std.shape)
print(X_test_std[0])

Y_pred = model.predict(X_test_std)
print(Y_pred) # all predicted value reated to respectivr test data

print(Y_pred.shape)
print(Y_pred[0]) #predicted probability for 1st samle
#where in below output 1st represent probability of 0 and 2nd represent probability of 1
# and whichever is grater that is our answer

# argmax function gives us index of max number
my_list1 = [0.25,0.56]
my_list2 = [0.56,0.25]

index_of_max_value1 = np.argmax(my_list1)
index_of_max_value2 = np.argmax(my_list2)

print(my_list1)
print(index_of_max_value1)

print(my_list2)
print(index_of_max_value2)

Y_pred_labels = [np.argmax(i) for i in Y_pred]
print(Y_pred_labels)

"""**Building the Predictive System**"""

input_data = (8.618,11.79,54.34,224.5,0.09752,0.05272,0.02061,0.007799,0.1683,0.07187,0.1559,0.5796,1.046,8.322,0.01011,0.01055,0.01981,0.005742,0.0209,0.002788,9.507,15.4,59.9,274.9,0.1733,0.1239,0.1168,0.04419,0.322,0.09026)

#change input_data to numpy array
input_data_as_numpy_array = np.asarray(input_data)

#reshape the numpy array as we are predicting for one data point
input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

#standardizing the input
input_data_std=scaler.transform(input_data_reshaped)

prediction = model.predict(input_data_std)
print(prediction)

prediction_label = [np.argmax(prediction)]
print(prediction_label)

if(prediction_label[0]==0):
  print('The tumor is Malignant')
else:
  print('The tumor is Benign')

