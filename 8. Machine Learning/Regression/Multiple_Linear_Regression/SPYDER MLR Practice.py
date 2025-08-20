## Import Libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

## Load the Dataset
dataset = pd.read_csv(r"C:\Users\shali\Desktop\Nit Data Science\6_Month_DS_Road_Map_2025\8. Machine Learning\Regression\Multiple_Linear_Regression\Investment.csv")

## Define Independent & Dependent Variables
x = dataset.iloc[:,:-1]
y = dataset.iloc[:,4]

# Encode Categorical Data (if any)
x=pd.get_dummies(x,dtype=int)

# Split the Dataset
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2, random_state=0)

# Train the Model
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(x_train, y_train)

# Predict and Compare
y_pred = regressor.predict(x_test)
print(y_pred)
comparison = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
print(comparison.head())

# Model Evaluation
bias = regressor.score(x_train, y_train)
variance = regressor.score(x_test, y_test)
print("Bias (Train Accuracy):", bias)
print("Variance (Test Accuracy):", variance)

# Model Parameters
m_slope = regressor.coef_
print(m_slope)

c_intercept = regressor.intercept_
print(c_intercept)

# Add Constant Column
#x = np.append(arr = np.ones((50,1)).astype(int), values= x, axis=1)
x = np.append(arr=np.full((50,1), 42467).astype(int), values=x, axis=1)

# Add Constant for OLS
#OLS (Ordinary Least Squares) from `statsmodels` requires a constant column to represent the intercept.

# Backward Elimination (Full Features)
import statsmodels.api as sm
x_opt = x [:, [0,1,2,3,4,5]]
regressor_OLS =sm.OLS(endog=y, exog=x_opt).fit()
regressor_OLS.summary()


# Remove Feature with Highest p-value
#Keep repeating this by removing the feature with the highest p-value above 0.05 until all remaining features are significant.
import statsmodels.api as sm
x_opt = x [:, [0,1,2,3,5]]
regressor_OLS =sm.OLS(endog=y, exog=x_opt).fit()
regressor_OLS.summary()

import statsmodels.api as sm
x_opt = x [:, [0,1,2,3]]
regressor_OLS =sm.OLS(endog=y, exog=x_opt).fit()
regressor_OLS.summary()

import statsmodels.api as sm
x_opt = x [:, [0,1,3]]
regressor_OLS =sm.OLS(endog=y, exog=x_opt).fit()
regressor_OLS.summary()

# Final Model after Elimination
import statsmodels.api as sm
x_opt = x [:, [0,1]]
regressor_OLS =sm.OLS(endog=y, exog=x_opt).fit()
regressor_OLS.summary()


