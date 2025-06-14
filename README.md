# Analyst Agent
## Overview
This project is an intelligent agent built using the Llama-4-Maverick model that can analyze various document types and engage in multi-turn Q&A conversations. It supports data visualization, document parsing, and advanced text analysis
## Features
### 📊 Data Analysis & Visualization
* CSV/Excel file processing
* Multiple plot types (line, scatter, bar, box)
* Statistical insights and correlations
### 📄 Document Processing
* PDF parsing with image extraction
* DOCX file support
* Advanced OCR for images
* Layout analysis for structured documents
### 💬 Intelligent Q&A
* Multi-turn conversation support
* Context-aware responses
* Data-driven insights

## Installation
1. Clone the repository:
```bash
git clone https://github.com/Sameerbeedi/Analyst-Agent
cd Analyst-Agent
```
2. Create a virtual environment(if required for windows):
```bash
python -m venv venv
.\venv\Scripts\activate
 ```

 3. Install dependecies 
 ```bash
pip install -r requirements.txt
 ```

 ## Configuration
1. Create an account at [Together AI](https://api.together.ai/signin)
2. Get your API key from [Together AI Dashboard](https://api.together.ai/settings/api-keys)
3. The API key is already configured in the code:
```python
together.api_key = "your-api-key"
```

 ## Usage
 1. Start the Streamlit App
 ```
 streamlit run main.py
 ```
 2. Upload your document (Supported formats):
 * Tables: CSV, XLSX
 * Documents: PDF, DOCX, TXT
 * Images: PNG, JPG, JPEG

 3. Ask questions about your document
 4. Explore visualizations and insights

## Resources
- [Together AI Documentation](https://docs.together.ai/)
- [Together AI Models](https://www.together.ai/products)
- [Together AI API Reference](https://docs.together.ai/reference/inference)

