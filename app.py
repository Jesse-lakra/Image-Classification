import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PIL import Image
import random

st.title("🐶🐱 Image Classification App")

# User email input
user_email = st.text_input("Enter your email to receive prediction result")

# Upload Image
image_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if image_file is not None:
    image = Image.open(image_file)
    st.image(image, caption="Uploaded Image")

    if st.button("Predict"):
        # Dummy prediction (replace with model prediction if using real model)
        classes = ["Dog", "Cat", "Other"]
        prediction = random.choice(classes)

        st.success(f"Prediction: {prediction}")

        # Send Email
        if user_email:
            try:
                sender_email = st.secrets["EMAIL"]
                sender_password = st.secrets["APP_PASSWORD"]

                msg = MIMEMultipart()
                msg["From"] = sender_email
                msg["To"] = user_email
                msg["Subject"] = "Image Classification Result"

                body = f"Hello,\n\nYour uploaded image is predicted as: {prediction}\n\nThank you."
                msg.attach(MIMEText(body, "plain"))

                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, user_email, msg.as_string())
                server.quit()

                st.success("Email sent successfully!")

            except Exception as e:
                st.error(f"Email sending failed: {e}")
        else:
            st.warning("Please enter your email address.")