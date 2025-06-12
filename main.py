import streamlit as st
import pandas as pd
import pdfplumber
import easyocr
import together
import matplotlib.pyplot as plt
from PIL import Image
import docx
import io
import numpy as np

# Set your Together API key
together.api_key = "6bf3732aa602bd98b4f7600e7b8e53d1bb3e4cb1a2fc9d6952c10593ea67e0d7"  # Replace with your actual key

# Initialize EasyOCR Reader
reader = easyocr.Reader(['en'])

# Function to ask LLaMA model via Together
def ask_llama(prompt):
    response = together.Complete.create(
        prompt=prompt,
        model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
        max_tokens=1024,
        temperature=0.7,
        top_p=0.9
    )
    return response['output']['choices'][0]['text'].strip()

# Function to parse uploaded file
def parse_file(file):
    name = file.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(file), "table"
    elif name.endswith(".xlsx"):
        return pd.read_excel(file), "table"
    elif name.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            text = '\n'.join([page.extract_text() or "" for page in pdf.pages])
        return text, "text"
    elif name.endswith(".docx"):
        doc = docx.Document(file)
        text = '\n'.join([para.text for para in doc.paragraphs])
        return text, "text"
    elif name.endswith(".txt"):
        return file.read().decode("utf-8"), "text"
    elif name.endswith((".png", ".jpg", ".jpeg")):
        image = Image.open(file).convert("RGB")
        result = reader.readtext(np.array(image))
        text = "\n".join([item[1] for item in result])
        return text, "text"
    else:
        return None, None

# Function to generate plots
def generate_plot(df, x_col, y_col):
    fig, ax = plt.subplots()
    ax.plot(df[x_col], df[y_col], marker='o')
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title(f"{y_col} vs {x_col}")
    st.pyplot(fig)

# Streamlit UI
st.set_page_config(page_title="Data Analyst Agent", layout="wide")
st.title("🧠 Data Analyst Agent (LLAMA-4 Maverick)")

uploaded_file = st.file_uploader(
    "Upload a document (.csv, .xlsx, .pdf, .docx, .txt, image)",
    type=["csv", "xlsx", "pdf", "docx", "txt", "png", "jpg", "jpeg"]
)

if uploaded_file:
    with st.spinner("Processing file..."):
        content, content_type = parse_file(uploaded_file)

    if content_type == "table":
        st.subheader("📊 Uploaded Data")
        st.dataframe(content)

        question = st.text_input("💬 Ask a question about the data")
        if question:
            data_preview = content.head(10).to_string()
            prompt = f"You are a data analyst. Analyze this data:\n{data_preview}\n\nAnswer the question:\n{question}"
            with st.spinner("Getting answer..."):
                response = ask_llama(prompt)
            st.markdown(f"**Answer:** {response}")

        st.subheader("📈 Create a visualization")
        x_col = st.selectbox("Select X-axis column", content.columns)
        y_col = st.selectbox("Select Y-axis column", content.columns)
        if st.button("Generate Plot"):
            generate_plot(content, x_col, y_col)

    elif content_type == "text":
        st.subheader("📄 Extracted Text")
        st.text_area("Document content:", content[:5000], height=300)

        question = st.text_input("💬 Ask a question about the document")
        if question:
            prompt = f"You are an expert analyst. Here is some document content:\n{content[:4000]}\n\nAnswer the question:\n{question}"
            with st.spinner("Thinking..."):
                response = ask_llama(prompt)
            st.markdown(f"**Answer:** {response}")
    else:
        st.error("Unsupported file type.")
