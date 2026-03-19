from bs4 import BeautifulSoup
import re
import math

class HtmlParser:
    def __init__(self):
        # Regex patterns for sensitive info
        self.email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
        self.btc_pattern = re.compile(r'\b(1[a-km-zA-HJ-NP-Z1-9]{25,34}|3[a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[a-zA-HJ-NP-Z0-9]{39,59})\b')

    def parse(self, html_content):
        """
        Parses HTML content to extract meaningful text, title, links, and sensitive data.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        title = soup.title.string if soup.title else 'No Title'
        title = title.strip() if title else 'No Title'
        
        text = soup.get_text(separator=' ')
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = ' '.join(chunk for chunk in chunks if chunk)

        # Extract sensitive info
        emails = list(set(self.email_pattern.findall(clean_text)))
        crypto_addresses = list(set(self.btc_pattern.findall(clean_text)))
        
        # Extract links
        links = []
        for a_tag in soup.find_all('a', href=True):
            links.append(a_tag['href'])

        return {
            'title': title,
            'text': clean_text,
            'emails': emails,
            'crypto_addresses': crypto_addresses,
            'links': list(set(links))
        }

if __name__ == "__main__":
    parser = HtmlParser()
    sample_html = "<html><title>Test Page</title><body>Contact admin@example.com for leaks. Send BTC to 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa.</body></html>"
    parsed = parser.parse(sample_html)
    print("Parsed Data:", parsed)
