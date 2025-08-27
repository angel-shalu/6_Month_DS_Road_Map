import streamlit as st
import numpy as np
import pickle

# Load both SLR and MLR models
mlr_model = pickle.load(open(r"C:\Users\shali\Desktop\DS_Road_Map\8. Machine Learning\Regression\MLR_House_Price_Predition\linear_regression_model.pkl",'rb'))
slr_model = pickle.load(open(r"C:\Users\shali\Desktop\DS_Road_Map\8. Machine Learning\Regression\SLR_House_Price_Prediction\linear_regression_model.pkl",'rb'))

# Set the title of the Streamlit App
st.title("House Price Prediction App")

# Add a brief description
st.write("This app predicts the house price using either Simple or Multiple Linear Regression model.")



# Sidebar for model selection and info
st.sidebar.markdown("# 🏡 House Price Options")
st.sidebar.markdown(
    """
    Welcome! Use the options below to customize your prediction experience.
    """
)
model_options = [
    "🔹 Simple Linear Regression",
    "🔸 Multiple Linear Regression"
]
# Attractive label for model selection
st.sidebar.markdown("<span style='color:#4F8BF9;font-size:18px;font-weight:bold;'>📊 <u>Choose Regression Model</u>:</span>", unsafe_allow_html=True)
model_choice = st.sidebar.selectbox(
    "",
    model_options,
    help="Select which regression model to use for prediction. SLR is simple and fast, MLR is more accurate with more features."
)
# Clean up model_choice for logic
if "Simple Linear Regression" in model_choice:
    model_choice = "Simple Linear Regression (SLR)"
else:
    model_choice = "Multiple Linear Regression (MLR)"

# Add a sidebar feature: Show Model Info
show_info = st.sidebar.checkbox("ℹ️ Show Model Info")
if show_info:
    info_choice = st.sidebar.radio(
        "Select Model Info to View:",
        ("Simple Linear Regression (SLR)", "Multiple Linear Regression (MLR)")
    )
    if info_choice == "Simple Linear Regression (SLR)":
        st.sidebar.markdown("""
        ### 🟦 Simple Linear Regression (SLR)
        - 📏 **Feature:** Only uses square footage (`sqft_living`)
        - ⚡ **Fast & Simple**
        - 🏷️ **Best for:** Quick, basic price estimates
        """)
    else:
        st.sidebar.markdown("""
        ### 🟩 Multiple Linear Regression (MLR)
        - 🏠 **Features:** Uses square footage, bedrooms, bathrooms, and floors
        - 🎯 **More Accurate**
        - 🏷️ **Best for:** Detailed, feature-rich price predictions
        """)


# Main input area with columns for a modern look
st.markdown("---")
st.markdown("### 🏠 Enter House Details")

if model_choice == "Multiple Linear Regression (MLR)":
    # All MLR inputs in one column
    with st.container():
        square_feet_living = st.number_input("Enter the square_feet of house:", min_value=500.0, max_value=270000.0, value=1000.0, step=500.0)
        bedroom = st.selectbox("Enter the Number of Bedrooms:", list(range(1, 11)), help="Choose number of bedrooms.")
        bathroom = st.selectbox("Enter the Number of Bathrooms:", list(range(1,11)), help="Choose number of bathrooms.")
        floors = st.selectbox("Select Floor:", list(range(1, 11)), help="Choose the floor number.")
else:
    # SLR input only
    square_feet_living = st.number_input("Enter the square_feet of house:", min_value=500.0, max_value=270000.0, value=1000.0, step=500.0)

# location input is not used in model, so we can remove or keep for info only
location = st.text_input("Location (City, Country):", help="Where are you based?")

# When the button is clicked, make prediction
if st.button("Predict the Price"):
    if model_choice == "Simple Linear Regression (SLR)":
        # SLR uses only square_feet_living
        input_features = np.array([[square_feet_living]])
        prediction = slr_model.predict(input_features)
        st.success(f"[SLR] The predicted price for {square_feet_living} sqft house is: ₹{prediction[0]:,.2f}")
    else:
        # MLR uses all features
        input_features = np.array([[square_feet_living, bedroom, bathroom, floors]])
        prediction = mlr_model.predict(input_features)
        st.success(f"[MLR] The predicted price for {square_feet_living} sqft, {bedroom} BedRoom, {bathroom} BathRoom, {floors} Floor House is: ₹{prediction[0]:,.2f}")

# Display information about the model
st.write("The model was trained using a dataset of price and features. Built by Shalini.")

