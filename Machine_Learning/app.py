
import streamlit as st
import pandas as pd
import joblib

# Load trained model and feature names
model = joblib.load("heart_model.pkl")
features = joblib.load("heart_features.pkl")

st.set_page_config(
    page_title="Heart Disease Prediction",
    page_icon="❤️",
    layout="centered"
)

st.title("❤️ Heart Disease Prediction")
st.write("Enter patient details to get the model's prediction.")

with st.form("patient_form"):

    age = st.number_input("Age", 1, 120, 50)
    sex = st.selectbox("Sex", [0, 1])
    cp = st.selectbox("Chest Pain Type (cp)", [0, 1, 2, 3])
    trestbps = st.number_input("Resting Blood Pressure", 50, 250, 130)
    chol = st.number_input("Cholesterol", 50, 700, 230)
    fbs = st.selectbox("Fasting Blood Sugar (fbs)", [0, 1])
    restecg = st.selectbox("Resting ECG (restecg)", [0, 1, 2])
    thalach = st.number_input("Maximum Heart Rate", 50, 250, 150)
    exang = st.selectbox("Exercise-Induced Angina (exang)", [0, 1])
    oldpeak = st.number_input("Oldpeak", 0.0, 10.0, 1.0, step=0.1)
    slope = st.selectbox("Slope", [0, 1, 2])
    ca = st.selectbox("Number of Major Vessels (ca)", [0, 1, 2, 3, 4])
    thal = st.selectbox("Thal", [0, 1, 2, 3])

    submitted = st.form_submit_button("Predict")

if submitted:
    patient = pd.DataFrame([{
        "age": age,
        "sex": sex,
        "cp": cp,
        "trestbps": trestbps,
        "chol": chol,
        "fbs": fbs,
        "restecg": restecg,
        "thalach": thalach,
        "exang": exang,
        "oldpeak": oldpeak,
        "slope": slope,
        "ca": ca,
        "thal": thal
    }])

    # Match the model's training feature order
    patient = patient[features]

    prediction = model.predict(patient)[0]

    st.subheader("Prediction Result")

    if prediction == 1:
        st.warning("Heart Disease: Predicted Positive")
    else:
        st.success("Heart Disease: Predicted Negative")

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(patient)[0]
        st.write("Model class probabilities:")
        st.json({
            str(label): round(float(prob), 4)
            for label, prob in zip(model.classes_, probabilities)
        })

    st.caption(
        "This is an experimental ML prediction, "
        "not a medical diagnosis or a guarantee of a heart attack."
    )
