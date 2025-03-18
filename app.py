import streamlit as st
from WebContentSummarizer import WebContentSummarizer

# Initialize summarizer
@st.cache_resource
def load_summarizer():
    return WebContentSummarizer()

summarizer = load_summarizer()

# Configure page
st.set_page_config(
    page_title="Web Content Summarizer",
    page_icon="📝",
    layout="centered"
)

# App header
st.title("Web Content Summarizer 🌐")
st.markdown("Enter a URL to extract content and generate an AI-powered summary")

# Input section
url = st.text_input("Enter URL:", placeholder="https://example.com/article")
process_button = st.button("Summarize")

# Initialize session state
if 'result' not in st.session_state:
    st.session_state.result = None

# Processing logic
if process_button and url:
    with st.spinner("Analyzing content and generating summary..."):
        st.session_state.result = summarizer.summarize_url(url)

# Display results
if st.session_state.result:
    result = st.session_state.result
    
    if result['error']:
        st.error(f"Error: {result['error']}")
    else:
        # Display extracted text
        st.subheader("Extracted Content")
        with st.expander("View full extracted text"):
            st.write(result['extracted_text'])
        
        # Display summary
        st.subheader("AI Summary")
        st.success(result['summary'])
        
        # Add download buttons
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="Download Summary",
                data=result['summary'],
                file_name="summary.txt"
            )
        with col2:
            st.download_button(
                label="Download Full Text",
                data=result['extracted_text'],
                file_name="full_content.txt"
            )