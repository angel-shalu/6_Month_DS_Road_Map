# Transformer to fill the missing values
# Data Preprocessing

# Importe the library
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Uploaded the dataset
dataset = pd.read_csv(r"C:\Users\shali\Desktop\Nit Data Science\MY_NIT_ALL_TASKS\3. AUGUST\ML\Data Processing\Dataset\Dataset for Data Processing.csv")

# We divided the data set into x and y
x = dataset.iloc[:,:-1].values    #  Separating Features and Target Variable   ## X contains input features (all columns except the last one)
y = dataset.iloc[:,3].values      ## y contains the target/output variable (column index 3 here, adjust if needed)



"""# Handling Missing Data using SimpleImputer
We can use SimpleImputer to fill the missing value with the median/mean of the column"""

# impute---Transformers for missing value imputation.
from sklearn.impute import SimpleImputer
imputer = SimpleImputer()
# # Create an imputer object with strategy = 'mean'
imputer = imputer.fit(x[:,1:3])           # Fit the imputer on columns 1 and 2 of X (index 1 and 2)
x[:,1:3] = imputer.transform(x[:,1:3])    # Replace missing values in X with the median values


"""
Median Startegy
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy="median")
imputer = imputer.fit(x[:,1:3])
x[:,1:3] = imputer.transform(x[:,1:3])

Mode startegy didi not work
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy="mode")
imputer = imputer.fit(x[:,1:3])
x[:,1:3] = imputer.transform(x[:,1:3])"""


"""# Encoding Categorical Data using LabelEncoder
Machine learning models do not understand text, so we need to convert text labels into numbers
"""
# Dummy var = 0, 1,2,3,4.... and( here we do cat data t0 var data)
from sklearn.preprocessing import LabelEncoder
labelencoder_x = LabelEncoder()
labelencoder_x.fit_transform(x[:,0])
x[:,0] = labelencoder_x.fit_transform(x[:,0])   # Encoding the first column of X 

labelencoder_y = LabelEncoder()
y = labelencoder_y.fit_transform(y)    # Encoding the target column y if it is categorical




"""Splitting the Dataset into Training and Testing Sets
We split the data so that the model can learn on training data and be tested on unseen test data"""

from sklearn.model_selection import train_test_split
# x_tarin,x_test,y_train,y_test = train_test_split(x,y, train_size=0.8, test_size=0.2)
#x_tarin,x_test,y_train,y_test = train_test_split(x,y, train_size=0.8) if we can write x_train it will automatically take x_test or vice versa

x_tarin,x_test,y_train,y_test = train_test_split(x,y, train_size=0.8, test_size=0.2,random_state=0)


