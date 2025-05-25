import streamlit as st
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.cluster.hierarchy import fcluster
import smtplib
from email.mime.text import MIMEText

# Load model and data
vectorizer = joblib.load('vectorizer.pkl')
Z = joblib.load('linkage_matrix.pkl')

# UI
st.title("Job Alert System - Karkidi.com")

user_email = st.text_input("Enter your email (sender):")
user_password = st.text_input("Enter your email password or app password:", type="password")
skill_interest = st.text_input("Enter your skill of interest (e.g., Python, NLP, SQL):")
recipient_email = st.text_input("Enter recipient email (where alerts will be sent):")

if st.button("Check for New Jobs & Subscribe"):
    if not user_email or not user_password or not recipient_email or not skill_interest:
        st.error("Please fill in all fields.")
    else:
        df = pd.read_csv("data/latest_jobs.csv")

        # Filter jobs with user skill
        filtered = df[df['Skills'].str.contains(skill_interest, case=False, na=False)]

        if not filtered.empty:
            st.success(f"Found {len(filtered)} jobs with your skill '{skill_interest}'")
            st.dataframe(filtered[['Title', 'Company', 'Location', 'Skills']])

            # Prepare email body
            body = "\n\n".join(filtered.apply(
                lambda row: f"{row['Title']} at {row['Company']} ({row['Location']})\nSkills: {row['Skills']}", axis=1))
            msg = MIMEText(body)
            msg['Subject'] = f"Job Alert: {skill_interest} positions found"
            msg['From'] = user_email
            msg['To'] = recipient_email

            # Send email using user-provided credentials
            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                    server.login(user_email, user_password)
                    server.send_message(msg)
                st.success("Email sent successfully!")
            except Exception as e:
                st.error(f"Failed to send email: {e}")
        else:
            st.warning(f"No new jobs found for skill: {skill_interest}")
