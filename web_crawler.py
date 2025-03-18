import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup, Comment
import readability
import re
from transformers import pipeline

class WebContentSummarizer:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        # Initialize summarization pipeline
        self.summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn",
            tokenizer="facebook/bart-large-cnn",
            framework="pt"
        )

    def _extract_text(self, url):
        """Extract and clean text content from webpage"""
        try:
            # Validate URL
            parsed = urlparse(url)
            if not all([parsed.scheme, parsed.netloc]):
                return {'error': 'Invalid URL format'}
            
            # Fetch content
            response = requests.get(url, headers=self.headers, timeout=10, verify=True)
            response.raise_for_status()
            
            if 'text/html' not in response.headers.get('Content-Type', ''):
                return {'error': 'Non-HTML content'}
            
            html = response.content
            
            # Extract main content
            try:
                doc = readability.Document(html)
                content_html = doc.summary()
            except:
                content_html = html

            # Clean text
            soup = BeautifulSoup(content_html, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['header', 'footer', 'nav', 'aside', 'script', 'style',
                               'noscript', 'meta', 'link', 'button', 'form', 'comment']):
                element.decompose()

            # Get visible text
            texts = soup.findAll(text=True)
            visible_text = filter(lambda t: t.parent.name not in ['pre', 'code'], texts)
            visible_text = filter(lambda x: not isinstance(x, Comment), visible_text)
            cleaned_text = ' '.join(t.strip() for t in visible_text if t.strip())
            
            # Final cleaning
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
            cleaned_text = re.sub(r'\[.*?\]', '', cleaned_text).strip()
            
            if not cleaned_text:
                return {'error': 'No text content found'}
            
            return {'text': cleaned_text}
            
        except Exception as e:
            return {'error': str(e)}

    def _chunk_text(self, text, max_length=1024):
        """Split text into chunks that fit model's max length"""
        words = text.split()
        chunks = []
        current_chunk = []
        
        for word in words:
            if len(current_chunk) + 1 <= max_length:
                current_chunk.append(word)
            else:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
            
        return chunks

    def summarize_url(self, url):
        """Process URL and generate summary"""
        result = {
            'url': url,
            'extracted_text': '',
            'summary': '',
            'error': None
        }
        
        # Extract text
        extraction = self._extract_text(url)
        if 'error' in extraction:
            result['error'] = extraction['error']
            return result
        
        text = extraction['text']
        result['extracted_text'] = text
        
        # Generate summary
        try:
            chunks = self._chunk_text(text)
            summaries = []
            
            for chunk in chunks:
                summary = self.summarizer(
                    chunk,
                    max_length=150,
                    min_length=30,
                    do_sample=False,
                    truncation=True
                )
                summaries.append(summary[0]['summary_text'])
            
            full_summary = ' '.join(summaries)
            
            # Create final concise summary
            final_summary = self.summarizer(
                full_summary,
                max_length=300,
                min_length=100,
                do_sample=False,
                truncation=True
            )[0]['summary_text']
            
            result['summary'] = final_summary
            
        except Exception as e:
            result['error'] = f"Summarization error: {str(e)}"
        
        return result

# Usage example
if __name__ == "__main__":
    summarizer = WebContentSummarizer()
    url = input("Enter URL to summarize: ")
    
    result = summarizer.summarize_url(url)
    
    if result['error']:
        print(f"Error: {result['error']}")
    else:
        print("\n=== Extracted Text (truncated) ===\n")
        print(result['extracted_text'][:1000] + "...\n")
        
        print("\n=== AI Summary ===\n")
        print(result['summary'])