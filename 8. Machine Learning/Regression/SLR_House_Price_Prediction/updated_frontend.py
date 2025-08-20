
import streamlit as st
import numpy as np
import pickle

# Custom CSS for beautiful design
st.markdown('''
    <style>
    body {background-color: #f5f7fa;}
    .main-card {
        background: #fff;
        border-radius: 18px;
        box-shadow: 0 4px 24px 0 rgba(0,0,0,0.10);
        padding: 2.5rem 2rem 2rem 2rem;
        margin-top: 2rem;
        margin-bottom: 2rem;
        max-width: 500px;
        margin-left: auto;
        margin-right: auto;
    }
    .main-title {
        color: #2d3a4b;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        color: #4f5d75;
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background: linear-gradient(90deg, #4f8cff 0%, #38b6ff 100%);
        color: white;
        border-radius: 8px;
        font-size: 1.1rem;
        font-weight: 600;
        padding: 0.6rem 2rem;
        margin-top: 1.2rem;
    }
    .stTextInput>div>input, .stNumberInput>div>input {
        border-radius: 8px;
        border: 1px solid #bfc9d9;
        padding: 0.5rem 1rem;
        font-size: 1.1rem;
    }
    </style>
''', unsafe_allow_html=True)

# Load the saved model
model = pickle.load(open(r"C:\Users\shali\Desktop\Nit Data Science\6_Month_DS_Road_Map_2025\8. Machine Learning\Regression\House_Price_Prediction\linear_regression_model.pkl",'rb'))

st.markdown(
    """
    <style>
    .main-title {
        font-size: 36px;
        color: #2E86C1;   /* Blue */
        text-align: center;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 18px;
        color: #117A65;   /* Green */
        text-align: center;
        margin-bottom: 20px;
    }
    .subtitle b {
        color: #E74C3C;   /* Red highlight for your name */
    }
    </style>
    <div class="main-title">🏡 House Price Prediction</div>
    <div class="subtitle">Predict the price of your dream house using advanced machine learning!<br>Built by <b>Shalini</b></div>
    """,
    unsafe_allow_html=True
)

# Custom CSS for styled input boxes
st.markdown(
    """
    <style>
    .input-card {
        background-color: #F8F9F9;  /* Light gray background */
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .input-label {
        font-weight: bold;
        color: #2E86C1;  /* Blue */
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Input widgets in styled columns
col1, col2 = st.columns(2)

with col1:
    square_feet_living = st.number_input("🏠 Square_feet of the House", min_value=500.0, max_value=270000.0, value=1000.0, step=500.0)
    bedroom = st.selectbox("🛏️ Number of Bedrooms", list(range(1, 11)), help="Choose number of bedrooms.")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    floors = st.selectbox("🏢 Floors", list(range(1, 11)), help="Choose the floor number.")
    location = st.text_input("📍 Location (City, Country)", help="Where are you based?")
    st.markdown('</div>', unsafe_allow_html=True)


# Predict button
if st.button("🚀 Predict Price"):
    sqft_input = np.array([[square_feet_living]])
    prediction = model.predict(sqft_input)

    st.markdown(
        f"""
        <style>
        .prediction-card {{
            background: linear-gradient(135deg, #e0f7fa, #e1f5fe);
            border-radius: 15px;
            padding: 20px;
            margin-top: 25px;
            text-align: center;
            font-family: 'Arial', sans-serif;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
            transition: 0.3s;
        }}
        .prediction-card:hover {{
            transform: scale(1.02);
            box-shadow: 0px 6px 18px rgba(0,0,0,0.25);
        }}
        .prediction-title {{
            font-size: 1.5rem;
            color: #0077b6;
            font-weight: 700;
        }}
        .prediction-value {{
            font-size: 2.2rem;
            color: #1b263b;
            font-weight: bold;
            margin-top: 10px;
        }}
        .details {{
            margin-top: 15px;
            font-size: 1rem;
            color: #37474f;
        }}
        .details span {{
            background: #f1f1f1;
            padding: 4px 10px;
            border-radius: 8px;
            margin: 0 4px;
        }}
        </style>

        <div class="prediction-card">
            <div class="prediction-title">
                🏡 Predicted Price for <b>{int(square_feet_living)}</b> sqft house:
            </div>
            <div class="prediction-value">
                💰₹{prediction[0]:,.2f}
            </div>
            <div class="details">
                🛏 Bedrooms: <span>{bedroom}</span> | 🏢 Floors: <span>{floors}</span> | 📍 Location: <span>{location if location else 'N/A'}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown('</div>', unsafe_allow_html=True)