import streamlit as st
import numpy as np
import pickle

# Load the saved model
model = pickle.load(open(r"C:\Users\shali\Desktop\Nit Data Science\6_Month_DS_Road_Map_2025\8. Machine Learning\Regression\MLR_House_Price_Predition\linear_regression_model.pkl",'rb'))

#Set the title of the Streamlit App
st.title("House Price Prediction App")

# Add a brief description
st.write("This app predicta the price based on square feet of the house using a linear regression model.")

# Add input widget for user to enter the square feet of the house
square_feet_living = st.number_input("Enter the sqft of house:", min_value=500.0, max_value=270000.0, value=1000.0, step=500.0)
bedroom = st.selectbox("Select Number of Bedrooms:", list(range(1, 11)),help="Choose number of bedrooms.")
bathroom = st.selectbox("Select Number of Bathrooms:", list(range(1,11)), help="Choose number of bathrooms.")
floors = st.selectbox("Select Floor:", list(range(1, 11)),help="Choose the floor number.")
# location input is not used in model, so we can remove or keep for info only
location = st.text_input("Location (City, Country):", help="Where are you based?")


# When the button is clicked, make prediction
if st.button("Predict the Price"):
    # Make a prediction using the trained model with all 4 features
    input_features = np.array([[square_feet_living, bedroom, bathroom, floors]])
    prediction = model.predict(input_features)
    # Display the result
    st.success(f"The predicted price for {square_feet_living} sqft, {bedroom} BedRoom, {bathroom} BathRoom, {floors} Floor House is: ₹{prediction[0]:,.2f}")
   
# Display information about the model
st.write("The model was trained using a dataset of price and Square_feet_living . Built model by Shalini")

