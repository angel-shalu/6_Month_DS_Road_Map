# Salary Prediction App

An interactive web application to predict salaries based on years of experience using a Simple Linear Regression (SLR) Machine Learning model. Built with Streamlit for a user-friendly experience.

## Features

- Predict salary based on user input (years of experience)
- Additional fields: education, industry, location (for future enhancements)
- Powered by a trained SLR model (scikit-learn)

## Files

- `frontend_code.py`: Main Streamlit app
- `app.py`: (Optional) Simpler version of the app
- `linear_regression_model.pkl`: Trained SLR model
- `Salary_Data.csv`: Dataset used for training

## How to Run

1. Install requirements:
   ```bash
   pip install streamlit numpy scikit-learn
   ```
2. Run the app:
   ```bash
   streamlit run frontend_code.py
   ```
3. Open the provided local URL in your browser.

## Model Details

- **Algorithm:** Simple Linear Regression
- **Input:** Years of Experience
- **Output:** Predicted Salary
- **Trained with:** `Salary_Data.csv`

## Credits

- Developed by Shalini
- Powered by Python, Streamlit, and scikit-learn
