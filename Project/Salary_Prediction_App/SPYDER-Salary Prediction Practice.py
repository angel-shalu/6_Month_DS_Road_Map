# Imported the library
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# Loaded the dataset:-
dataset = pd.read_csv(r"C:\Users\shali\Desktop\Nit Data Science\6_Month_DS_Road_Map_2025\8. Machine Learning\Regression\Salary_Prediction_App\Salary_Data.csv")
# Returns an Index object containing all column names in your DataFrame.
dataset.columns
# Returns the row index labels of your DataFrame.
dataset.index
# Returns a tuple (number_of_rows, number_of_columns).
dataset.shape
# Prints a summary of the DataFrame:
dataset.info()
# Returns summary statistics for all numeric columns by default:
dataset.describe()
# Shows the first 5 rows of the DataFrame
dataset.head()
# Shows the first 5 rows of the DataFrame (default), so you can quickly check the top records.
dataset.tail()


# Separate features and target:-
x = dataset.iloc[:,:-1]     # Input variable (Years of Experience)
y = dataset.iloc[:,-1]      # Target variable (Salary)


# Split into training and testing sets
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(x,y, train_size=0.8, random_state=0)


# Import and train the model:-
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()   # We create the linear regression model
regressor.fit(x_train, y_train)  # We fit the model using the training data


# Predict test set:-
y_pred = regressor.predict(x_test)  # Using the trained model to make predictions on test data

# Compare actual vs predicted:-
comparison = pd.DataFrame({'Actual': y_test, 'Predict': y_pred})   # Creating a DataFrame to compare actual and predicted salaries


# Visualize the results:-
# Red points are actual test data, blue line is the regression prediction
plt.scatter(x_test, y_test, color="red")
plt.plot(x_train, regressor.predict(x_train), color='blue')   # here we can pass x_test or x_train both
#plt.plot(x_test, regressor.predict(x_test), color='blue')
plt.title("Salary vs Experience(Test set)")
plt.xlabel("Year of Experience")
plt.ylabel("Salry")
plt.show()


# Calculate Slope (m) and Intercept (c):-
# Get the slope (m) of the regression line
m_slope = regressor.coef_
# Get the intercept (c) of the regression line
c_intercept = regressor.intercept_


# Predict salary on unseen data
#Let's Predict for 12 and 20 years of experience
# Using the formula: Y = mX + c
# Predict for 12 years
yr_12 = (m_slope * 12) + c_intercept
yr_12
# Predict for 20 years
yr_20 = (m_slope * 20) + c_intercept
yr_20



bias = regressor.score(x_train, y_train)
bias

variance = regressor.score(x_train, y_train)
variance



# STATS FOR ML
# stats for slr ml

dataset.mean()
dataset["Salary"].mean()

dataset.median()
dataset["Salary"].median()

dataset.mode()
dataset["Salary"].mode()

dataset.var()
dataset["Salary"].var()
dataset["Salary"].std()

from scipy.stats import variation
variation(dataset.values)   #this will give cv of the entire dataframe
variation(dataset["Salary"])  #this will give cv of the particular column

dataset.corr()   #this will give the coreelation of the entire dataframe
dataset["Salary"].corr(dataset["YearsExperience"])    # this will give the corelation beytween there two dataframe

dataset.skew()
dataset["Salary"].skew()

dataset.sem()   # his will give the standard error in the entire dataframe
dataset["Salary"].sem()  # this will give the standard error on the particular column

import scipy.stats as stats
dataset.apply(stats.zscore)
stats.zscore(dataset["Salary"])

a = dataset.shape[0]
b = dataset.shape[1]
degree_of_freedom = a-b
print(degree_of_freedom)


#SSR  
y_mean = np.mean(y)
SSR = np.sum((y_pred-y_mean)**2)
print(SSR)

#SSE 
y = y[0:6]
SSE = np.sum((y-y_pred)**2)
print(SSE)

#SST
mean_total = np.mean(dataset.values)
SST = np.sum((dataset.values-mean_total)**2)
print(SST)

#R2
r_square = 1-SSR/SST
print(r_square)





















