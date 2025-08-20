import numpy as np  
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pickle

# Load the dataset
dataset = pd.read_csv(r"C:\Users\shali\Desktop\Nit Data Science\6_Month_DS_Road_Map_2025\8. Machine Learning\Regression\MLR_House_Price_Predition\House_data.csv")

# Drop non-numeric / unnecessary columns (like 'id' and 'date')
dataset = dataset.drop(columns=['id', 'date'], errors='ignore', axis=1)

# Independent variable(s) (X) and dependent variable (y)
X = dataset[['sqft_living', 'bedrooms', 'bathrooms', 'floors']].values
y = dataset['price'].values

# Split the dataset into training and testing sets (80-20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)

# Train the model
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Predict the test set
y_pred = regressor.predict(X_test)

#comparision for y_test vs y_pred
comparison = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
print(comparison)

# Visualize the training set
# Predicted vs Actual values (Test set)
plt.scatter(y_test, y_pred, color='blue')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')  # perfect prediction line
plt.title('Actual vs Predicted Prices')
plt.xlabel('Actual Price')
plt.ylabel('Predicted Price')
plt.show()


residuals = y_test - y_pred
plt.scatter(y_pred, residuals, color='purple')
plt.axhline(y=0, color='red', linestyle='--')
plt.title('Residuals vs Predicted Values')
plt.xlabel('Predicted Price')
plt.ylabel('Residuals (Actual - Predicted)')
plt.show()


feature_names = ['sqft_living', 'bedrooms', 'bathrooms', 'floors']
coefficients = regressor.coef_
plt.bar(feature_names, coefficients, color='teal')
plt.title('Feature Importance (Regression Coefficients)')
plt.xlabel('Features')
plt.ylabel('Coefficient Value')
plt.show()

#understanding the distribution with seaborn
with sns.plotting_context("notebook",font_scale=2.5):
    g = sns.pairplot(dataset[['sqft_lot','sqft_above','price','sqft_living','bedrooms']], 
                 hue='bedrooms', palette='tab20',size=6)
g.set(xticklabels=[])

# Predict price for sqft_living using the trained model
# Example houses (n_samples=1, n_features=4)
sample_house1 = [[2207, 3, 2, 1]]   # [[sqft_living, bedrooms, bathrooms, floors]]
sample_house2 = [[8870, 5, 4, 2]]
# Predictions
y_house1 = regressor.predict(sample_house1)
y_house2 = regressor.predict(sample_house2)
print(f"Predicted price for House1: ${y_house1[0]:,.2f}")
print(f"Predicted price for House2: ${y_house2[0]:,.2f}")


# Check model performance
bias = regressor.score(X_train, y_train)      # R² on train
variance = regressor.score(X_test, y_test)    # R² on test
train_mse = mean_squared_error(y_train, regressor.predict(X_train))
test_mse = mean_squared_error(y_test, y_pred)

print(f"Training Score (R^2): {bias:.2f}")
print(f"Testing Score (R^2): {variance:.2f}")
print(f"Training MSE: {train_mse:.2f}")
print(f"Test MSE: {test_mse:.2f}")

# Save the trained model to disk
import pickle
filename = 'linear_regression_model.pkl'
with open(filename, 'wb') as file:
     pickle.dump(regressor, file)
     
print("Model has been pickled and saved as linear_regression_model.pkl")
import os
os.getcwd()

import numpy as np
import statsmodels.api as sm

def backwardElimination(X, y, SL=0.05):
    X = sm.add_constant(X)  # add intercept
    numVars = X.shape[1]
    for i in range(numVars):
        regressor = sm.OLS(y, X).fit()
        max_pval = max(regressor.pvalues)
        if max_pval > SL:
            max_index = np.argmax(regressor.pvalues)
            X = np.delete(X, max_index, 1)  # remove feature with highest p-value
        else:
            break
    print(regressor.summary())
    return X

# Example usage
SL = 0.05
X_opt = X[:, :18]   # your chosen features
X_modeled = backwardElimination(X_opt, y, SL)
