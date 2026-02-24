import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
from PIL import Image

st.title("🐶🐱 Image Classification App")

# Load trained model
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model("model.h5")
    return model

model = load_model()

# Upload dataset
st.header("Upload Dataset (CSV or Excel)")
uploaded_file = st.file_uploader("Upload your dataset", type=["csv", "xlsx"])

if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("Dataset Uploaded Successfully!")
    st.write("Dataset Preview:")
    st.dataframe(df.head())

    # Filter detector_enabled
    if "detector_enabled" in df.columns:
        detect_only = st.checkbox("Show Only Detector Enabled (1)")
        if detect_only:
            df = df[df["detector_enabled"] == 1]
            st.write("Filtered Dataset:")
            st.dataframe(df.head())

# Upload Image
st.header("Upload Image for Classification")
image_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if image_file is not None:
    image = Image.open(image_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Preprocess image
    img = image.resize((128, 128))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img)
    class_names = ["Cat", "Dog", "Other"]

    predicted_class = class_names[np.argmax(prediction)]
    confidence = np.max(prediction)

    st.success(f"Prediction: {predicted_class}")
    st.info(f"Confidence: {confidence:.2f}")