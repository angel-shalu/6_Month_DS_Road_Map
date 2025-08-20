import streamlit as st
import numpy as np
import pickle

# Load the saved model
model = pickle.load(open(r"C:\Users\shali\Desktop\Nit Data Science\6_Month_DS_Road_Map_2025\8. Machine Learning\Regression\House_Price_Prediction\linear_regression_model.pkl",'rb'))

#Set the title of the Streamlit App
st.title("House Price Prediction App")

# Add a brief description
st.write("This app predicta the price based on square feet of the house using a linear regression model.")

# Add input widget for user to enter the square feet of the house
square_feet_living = st.number_input("Enter the sqft of house:", min_value=500.0, max_value=270000.0, value=1000.0, step=500.0)
floors = st.selectbox("Select floor:", ["First", "Second", "Third", "Four", "Other"], help="Choose the floor number.")
bedrooms = st.selectbox("Select Number od bedrooms:",["1", "2", "3", "4,"], help="Choose number of the bedrooms.")
location = st.text_input("Location (City, Country):", help="Where are you based?")

# When the button is clicked, make prediction
if st.button("Predict Price"):
    # Make a preduction using the trained model
    sqft_input = np.array([[square_feet_living]])
    prediction = model.predict(sqft_input)
    
    # Display the result
    st.success(f"The predicted price for {square_feet_living} House is: ${prediction[0]:,.2f}")
   
# Display information about the model
st.write("The model was trained using a dataset of price and Square_feet_living . Built model by Shalini")

