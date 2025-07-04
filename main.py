import streamlit as st
import together
import pandas as pd
import numpy as np
from PIL import Image
import easyocr
import PyPDF2
from docx import Document
import matplotlib.pyplot as plt


# API Configuration
together.api_key = "6bf3732aa602bd98b4f7600e7b8e53d1bb3e4cb1a2fc9d6952c10593ea67e0d7" 

# Initialize EasyOCR Reader
reader = easyocr.Reader(['en'])

# Function to ask LLaMA model via Together
def ask_llama(prompt):
    try:
        response = together.Complete.create(
            model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
            prompt=prompt,
            max_tokens=500,
            temperature=0.7,
            top_p=0.95,
        )
        # Correct response parsing
        if response and 'choices' in response:
            return response['choices'][0]['text'].strip()
        else:
            st.error("Unexpected response format from Together AI")
            return None
    except Exception as e:
        st.error(f"Error communicating with Together AI: {str(e)}")
        return None


# Function to parse uploaded file
def parse_file(file):
    name = file.name.lower()
    if name.endswith((".csv", ".xlsx")):
        df = pd.read_csv(file) if name.endswith(".csv") else pd.read_excel(file)
        return df, "table"
    elif name.endswith((".txt", ".log", ".md")):
        return file.read().decode("utf-8"), "text"
    elif name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text, "text"
        except Exception as e:
            st.error(f"Error reading PDF: {str(e)}")
            return None, None
    elif name.endswith(".docx"):
        try:
            doc = Document(file)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text, "text"
        except Exception as e:
            st.error(f"Error reading DOCX: {str(e)}")
            return None, None
    elif name.endswith((".png", ".jpg", ".jpeg")):
        img = Image.open(file)
        reader = easyocr.Reader(['en'])
        result = reader.readtext(np.array(img))
        text = ' '.join([item[1] for item in result])
        return text, "text"
    else:
        st.error(f"Unsupported file type: {name}")
        return None, None


# Function to generate plots
def generate_plot(data, x_col, y_col):
    try:
        fig, ax = plt.subplots()
        if isinstance(data, pd.DataFrame):
            data.plot(x=x_col, y=y_col, ax=ax)
        else:
            st.error("Data must be a pandas DataFrame for plotting")
            return
        
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.title(f"{y_col} vs {x_col}")
        
        # Display plot in Streamlit
        st.pyplot(fig)
        plt.close()
    except Exception as e:
        st.error(f"Error generating plot: {str(e)}")

# Streamlit UI
st.set_page_config(page_title="Data Analyst Agent", layout="wide")
st.title("🧠 Data Analyst Agent")

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
