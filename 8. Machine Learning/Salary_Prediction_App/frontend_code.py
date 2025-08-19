import streamlit as st
import numpy as np
import pickle

# Custom CSS for beautiful landing page
st.markdown('''
    <style>
    body {
        margin: 0;
        padding: 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #232526 0%, #000000 100%);
        min-height: 100vh;
        animation: gradientBG 10s ease infinite;
    }
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    .container {
        max-width: 650px;
        margin: 60px auto;
        background: rgba(30, 30, 30, 0.85);
        border-radius: 22px;
        box-shadow: 0 8px 32px 0 rgba(0,0,0,0.45);
        padding: 48px 36px 36px 36px;
        text-align: center;
        backdrop-filter: blur(6px);
        border: 1.5px solid rgba(255,255,255,0.08);
    }
    .main-header h1 {
        font-size: 2.7rem;
        color: #fff;
        margin-bottom: 10px;
        letter-spacing: 1px;
        text-shadow: 0 2px 8px #000a;
    }
    .main-header p {
        color: #b0b0b0;
        font-size: 1.25rem;
        margin-bottom: 30px;
    }
    .start-btn {
        display: inline-block;
        padding: 16px 44px;
        background: linear-gradient(90deg, #ff512f 0%, #dd2476 100%);
        color: #fff;
        font-size: 1.25rem;
        border: none;
        border-radius: 30px;
        text-decoration: none;
        font-weight: bold;
        box-shadow: 0 4px 14px 0 rgba(221,36,118,0.18);
        transition: background 0.3s, transform 0.2s;
        margin-top: 22px;
        letter-spacing: 1px;
    }
    .start-btn:hover {
        background: linear-gradient(90deg, #dd2476 0%, #ff512f 100%);
        transform: translateY(-3px) scale(1.07);
    }
    .icon {
        font-size: 2.5rem;
        color: #ff512f;
        margin-bottom: 10px;
        animation: bounce 2s infinite;
    }
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    .fun-fact {
        color: #ffd700;
        font-size: 1.1rem;
        margin: 18px 0 0 0;
        font-style: italic;
    }
    footer {
        margin-top: 40px;
        color: #b0b0b0;
        font-size: 1rem;
    }
    </style>
''', unsafe_allow_html=True)

# --- Navigation logic ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

if st.session_state.page == 'landing':
    st.markdown('''
    <div class="container">
        <header class="main-header">
            <div class="icon">💼</div>
            <h1>Welcome to the Salary Prediction App</h1>
            <p>Predict your salary based on your Years of Experience using Simple Linear Regression Machine Learing Model!</p>
        </header>
        <main>
            <form action="#" method="post">
                <button type="submit" name="start" class="start-btn" style="cursor:pointer;width:70%;margin:0 auto;">Start Predicting</button>
            </form>
            <div class="fun-fact">✨ Fun Fact: Did you know? The first regression analysis was published in 1805 by Adrien-Marie Legendre! ✨</div>
        </main>
        <footer>
          <p>Made By <strong style="color: Red;">Shalini</strong> | Powered by <strong style="color: green;">Machine Learning</strong></p>
        </footer>
    </div>
    ''', unsafe_allow_html=True)
    # Streamlit workaround for button in HTML
    if st.button("Start Predicting", key="start-btn-real"):
        st.session_state.page = 'predict'

if st.session_state.page == 'predict':
    st.header("Salary Prediction")
    st.write("This app predicts the salary based on years of experience using a linear regression model.")

    model = pickle.load(open(r"C:\Users\shali\Desktop\Nit Data Science\6_Month_DS_Road_Map_2025\8. Machine Learning\Regression\Salary_Prediction_App\linear_regression_model.pkl",'rb'))

    col1, col2 = st.columns([2, 1])
    with col1:
        years_of_experience = st.number_input("Enter Years of Experience:", min_value=0.0, max_value=50.0, value=1.0, step=0.1, help="How many years have you worked?")
        education = st.selectbox("Select Education Level:", ["High School", "Bachelor's", "Master's", "PhD"], help="Choose your highest education completed.")
        industry = st.selectbox("Select Industry:", ["IT", "Finance", "Healthcare", "Education", "Other"], help="Choose your industry.")
        location = st.text_input("Location (City, Country):", help="Where are you based?")
        if st.button("Predict Salary"):
            # For demo, only years_of_experience is used in prediction
            experience_input = np.array([[years_of_experience]])
            prediction = model.predict(experience_input)
            st.success(f"The predicted salary for {years_of_experience} years of experience is: ${prediction[0]:,.2f}")
            st.info(f"Education: {education} | Industry: {industry} | Location: {location if location else 'N/A'}")
    with col2:
        st.image("https://img.icons8.com/ios-filled/200/ffffff/money-bag.png", width=120)

    st.write("The model was trained using a dataset of salaries and years of experience. Built by Shalini.")
    st.markdown('<div style="color:#ffd700;font-size:1.05rem;margin-top:18px;">💡 Tip: More features coming soon! Stay tuned for updates.</div>', unsafe_allow_html=True)