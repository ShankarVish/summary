import streamlit as st
import sys
import os
import nbformat
from nbconvert import PythonExporter
import importlib.util

# Convert and load web_crawler.ipynb dynamically
notebook_path = os.path.join(os.path.dirname(__file__), "web_crawler.ipynb")
script_path = os.path.join(os.path.dirname(__file__), "web_crawler.py")

if os.path.exists(notebook_path):
    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook_content = nbformat.read(f, as_version=4)
    
    exporter = PythonExporter()
    script_content, _ = exporter.from_notebook_node(notebook_content)

    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script_content)

# Import the dynamically created module
spec = importlib.util.spec_from_file_location("web_crawler", script_path)
web_crawler = importlib.util.module_from_spec(spec)
sys.modules["web_crawler"] = web_crawler
spec.loader.exec_module(web_crawler)

# Initialize summarizer
summarizer = web_crawler.WebContentSummarizer()

# Streamlit UI
st.title("Web Content Summarizer")
st.write("Enter a URL to extract and summarize its content.")

# Input field for URL
url = st.text_input("Enter URL:")

if st.button("Summarize"):
    if url:
        with st.spinner("Extracting and summarizing..."):
            result = summarizer.summarize_url(url)
            
            if result.get('error'):
                st.error(f"Error: {result['error']}")
            else:
                st.subheader("Extracted Text (truncated)")
                st.text_area("Extracted Content", result.get('extracted_text', '')[:1000] + "...", height=200)
                
                st.subheader("AI-Generated Summary")
                st.text_area("Summary", result.get('summary', ''), height=150)
    else:
        st.warning("Please enter a valid URL.")
