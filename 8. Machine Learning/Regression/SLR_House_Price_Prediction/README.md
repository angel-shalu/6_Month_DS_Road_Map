# House Price Prediction App

This is a simple web application built with Streamlit that predicts house prices based on user input features. The app uses a trained linear regression model to estimate the price of a house.

## Features
- Predicts house price based on square feet, number of bedrooms, floors, and location.
- User-friendly interface with input widgets for all features.
- Displays the predicted price and summary of selected features.

## How to Run
1. Make sure you have Python installed.
2. Install the required packages:
   ```bash
   pip install streamlit numpy
   ```
3. Place the trained model file `linear_regression_model.pkl` in the same directory as `app.py`.
4. Run the app using Streamlit:
   ```bash
   streamlit run app.py
   ```
5. Open the provided local URL in your browser to use the app.

## File Structure
- `app.py` : Main Streamlit application file.
- `linear_regression_model.pkl` : Trained linear regression model (required for predictions).

## Example Usage
- Enter the square footage of the house.
- Select the number of bedrooms and floors.
- Enter the location (city, country).
- Click **Predict Price** to see the estimated house price.

## Author
Built by Shalini
