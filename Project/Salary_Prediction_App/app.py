import streamlit as st
import numpy as np
import pickle

# Load the saved model
model = pickle.load(open(r"C:\Users\shali\Desktop\Nit Data Science\6_Month_DS_Road_Map_2025\8. Machine Learning\Regression\Salary_Prediction_App\linear_regression_model.pkl",'rb'))

#Set the title of the Streamlit App
st.title("Salary Prediction App")

# Add a brief description
st.write("This app predicta the salary based on years of experience using a linear regression model.")

# Add input widget for user to enter years of experiences
years_of_experience = st.number_input("Enter Years of Experience:", min_value=0.0, max_value=50.0, value=1.0, step=0.1)

# When the button is clicked, make prediction
if st.button("Predict Salary"):
    # Make a preduction using the trained model
    experience_input = np.array([[years_of_experience]])
    prediction = model.predict(experience_input)
    
    # Display the result
    st.success(f"The predicted salary for {years_of_experience} years of experience is: ${prediction[0]:,.2f}")
   
# Display information about the model
st.write("The model was trained using a dataset of salaries and years of experience.built model by Shalini")