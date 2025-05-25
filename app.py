# app.py
import streamlit as st
import joblib
import numpy as np

# Load model
model = joblib.load('model.pkl')

st.title("Clustering Model App")
st.write("Enter the features to predict the cluster.")

# Example: assuming your model expects 3 features
feature1 = st.number_input("Feature 1", value=0.0)
feature2 = st.number_input("Feature 2", value=0.0)
feature3 = st.number_input("Feature 3", value=0.0)

if st.button("Predict Cluster"):
    input_data = np.array([[feature1, feature2, feature3]])
    prediction = model.predict(input_data)
    st.success(f"Predicted Cluster: {prediction[0]}")
