import streamlit as st
import pickle

# ---------------------------------------------------
# ✅ GLOBAL CSS + BACKGROUND VIDEO  (WORKING FIX)
# ---------------------------------------------------
st.markdown("""
<style>

html, body, [class*="css"]  {
    height: 100%;
    margin: 0;
    padding: 0;
}

/* ✅ Full-screen background video */
video#bg-video {
    position: fixed;
    top: 0;
    left: 0;
    min-width: 100%;
    min-height: 100%;
    width: auto;
    height: auto;
    z-index: -999;
    object-fit: cover;
    filter: brightness(0.40);
}

/* ✅ Make Streamlit containers transparent */
.stApp {
    background: transparent !important;
}

.main-content {
    text-align: center;
    margin-top: 120px;
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

/* ✅ Icon */
.icon {
    font-size: 3.8rem;
    margin-bottom: 18px;
}

/* ✅ Typewriter Effect */
.typewriter h1 {
    font-size: 2.8rem;
    white-space: nowrap;
    overflow: hidden;
    width: fit-content;
    margin: 0 auto;
    letter-spacing: 1px;
    animation: typing 3s steps(40, end);
}

@keyframes typing {
    from { width: 0; }
    to { width: 100%; }
}

/* ✅ Subtitle */
.subtitle {
    font-size: 1.3rem;
    margin-top: 15px;
    opacity: 0.92;
}

/* ✅ White CTA Button */
.start-btn {
    display: inline-block;
    padding: 16px 44px;
    background: white;
    color: black !important;
    text-decoration: none !important;
    font-size: 1.25rem;
    font-weight: bold;
    border-radius: 28px;
    margin-top: 28px;
    transition: 0.3s;
    box-shadow: 0 4px 15px rgba(255,255,255,0.2);
}
.start-btn:hover {
    transform: scale(1.08);
    background: #efefef;
}

/* ✅ Fun fact */
.fun-fact {
    font-size: 1.15rem;
    margin-top: 22px;
    color: #ffd700;
    font-style: italic;
}

/* ✅ Footer */
footer {
    margin-top: 40px;
    color: #eaeaea;
    font-size: 1rem;
}

</style>
""", unsafe_allow_html=True)



# ---------------------------------------------------
# ✅ NAVIGATION
# ---------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = st.query_params.get("page", "landing")
else:
    new_page = st.query_params.get("page")
    if new_page and new_page != st.session_state.page:
        st.session_state.page = new_page


def go_to(page):
    st.session_state.page = page
    st.query_params["page"] = page
    st.rerun()



# ---------------------------------------------------
# ✅ LOAD MODEL
# ---------------------------------------------------
MODEL_PATH = r"C:\Users\shali\Desktop\DS_Road_Map\Project\SLR_Salary_Prediction_App\linear_regression_model.pkl"

@st.cache_resource
def load_model(path):
    with open(path, "rb") as f:
        return pickle.load(f)



# ---------------------------------------------------
# ✅ ✅ LANDING PAGE WITH WORKING BACKGROUND VIDEO ✅ ✅
# ---------------------------------------------------
if st.session_state.page == "landing":

    # ✅ Background Video (NEW ML-THEME)
    st.html("""
        <video autoplay muted loop id="bg-video">
            <source src="https://videos.pexels.com/video-files/3180083/3180083-hd_1920_1080_25fps.mp4" type="video/mp4">
        </video>
    """)

    # ✅ UI on top of video
    st.html("""
        <div class="main-content">

            <div class="icon">💼</div>

            <div class="typewriter">
                <h1>Welcome to the Salary Prediction App</h1>
            </div>

            <p class="subtitle">
                Predict your salary instantly using Machine Learning.
            </p>

            <a href="?page=predict" class="start-btn">Start Predicting</a>

            <div class="fun-fact">
                ✨ Did you know? Regression analysis began in 1805 with Legendre! ✨
            </div>

            <footer>
                Made By <strong style='color:red;'>Shalini</strong> |
                Powered by <strong style='color:lightgreen;'>Machine Learning</strong>
            </footer>

        </div>
    """)

    nav = st.query_params.get("page")
    if nav and nav != "landing":
        go_to(nav)



# ---------------------------------------------------
# ✅ ✅ PREDICTION PAGE
# ---------------------------------------------------
elif st.session_state.page == "predict":

    st.header("Salary Prediction")

    try:
        model = load_model(MODEL_PATH)
    except Exception as e:
        st.error(f"Model loading failed: {e}")
        st.stop()

    col1, col2 = st.columns([2, 1])

    with col1:
        years = st.number_input("Years of Experience:", 0.0, 50.0, 1.0, 0.1)
        edu = st.selectbox("Education:", ["High School", "Bachelor's", "Master's", "PhD"])
        ind = st.selectbox("Industry:", ["IT", "Finance", "Healthcare", "Education", "Other"])
        loc = st.text_input("Location:")

        if st.button("Predict Salary"):
            predicted_salary = float(model.predict([[years]])[0])
            st.success(f"Predicted Salary: ₹{predicted_salary:,.2f}")
            st.info(f"Education: {edu} | Industry: {ind} | Location: {loc or 'N/A'}")

    with col2:
        st.image("https://img.icons8.com/ios-filled/200/ffffff/money-bag.png", width=120)

    if st.button("⬅ Back to Home"):
        st.query_params.clear()
        go_to("landing")
