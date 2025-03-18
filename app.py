import streamlit as st
import sys
import os

# Ensure the script can find web_crawler.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from web_crawler import WebContentSummarizer  # Importing from web_crawler.py

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
            
            if result['error']:
                st.error(f"Error: {result['error']}")
            else:
                st.subheader("Extracted Text (truncated)")
                st.text_area("Extracted Content", result['extracted_text'][:1000] + "...", height=200)
                
                st.subheader("AI-Generated Summary")
                st.text_area("Summary", result['summary'], height=150)
    else:
        st.warning("Please enter a valid URL.")

# Run the app with: `streamlit run app.py