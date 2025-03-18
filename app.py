import streamlit as st
import sys
import os
import nbformat
from nbconvert import PythonExporter

# Ensure the script can find web_crawler.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Check if web_crawler.py exists; otherwise, load from web_crawler.ipynb
if os.path.exists("web_crawler.py"):
    from web_crawler import WebContentSummarizer
else:
    # Load the notebook
    with open("web_crawler.ipynb", "r") as f:
        notebook_content = nbformat.read(f, as_version=4)

    # Convert notebook to Python code
    exporter = PythonExporter()
    python_code, _ = exporter.from_notebook_node(notebook_content)

    # Execute the code
    exec(python_code, globals())

# Initialize summarizer
summarizer = WebContentSummarizer()

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

# Run the app with: `streamlit run app.py`
