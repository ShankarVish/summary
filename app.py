import streamlit as st
from web_crawler import WebContentSummarizer

# Initialize summarizer with caching
@st.cache_resource
def load_summarizer():
    return WebContentSummarizer()

summarizer = load_summarizer()

# Streamlit UI Configuration
st.set_page_config(
    page_title="Web Content Summarizer",
    page_icon="🌐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS styling
st.markdown("""
    <style>
    .reportview-container {
        background: #f0f2f6;
    }
    .sidebar .sidebar-content {
        background: #ffffff;
    }
    h1 {
        color: #1f77b4;
    }
    </style>
    """, unsafe_allow_html=True)

# Main App Interface
st.title("🌐 Web Content Summarizer")
st.markdown("""
    *Extract key content and generate AI-powered summaries from any webpage*  
    🔗 Enter a valid URL below to get started
""")

# URL Input Section
url = st.text_input("Website URL:", 
                   placeholder="https://example.com/article",
                   key="url_input")

# Main Processing Function
def process_url(url):
    with st.spinner("🕵️ Analyzing website content..."):
        result = summarizer.summarize_url(url)
        
        if result['error']:
            st.error(f"❌ Error: {result['error']}")
            return
            
        with st.container():
            st.subheader("📄 Extracted Content")
            with st.expander("View full extracted text", expanded=False):
                st.text_area("Full Content", 
                            value=result['extracted_text'],
                            height=300,
                            label_visibility="collapsed")
            
            st.subheader("🤖 AI Summary")
            st.success(result['summary'])
            
            # Download buttons
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="📥 Download Summary",
                    data=result['summary'],
                    file_name="website_summary.txt",
                    mime="text/plain"
                )
            with col2:
                st.download_button(
                    label="📥 Download Full Text",
                    data=result['extracted_text'],
                    file_name="full_content.txt",
                    mime="text/plain"
                )

# Handle form submission
if st.button("🚀 Generate Summary", use_container_width=True):
    if url:
        process_url(url)
    else:
        st.warning("⚠️ Please enter a valid URL")

# Footer
st.markdown("---")
st.markdown("""
    *Built with ❤️ using Streamlit • HuggingFace Transformers • BeautifulSoup*
""")