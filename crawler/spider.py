import logging
from .tor_request import TorSession

class Spider:
    def __init__(self, proxy_url="socks5h://127.0.0.1:9050"):
        self.tor_session = TorSession(proxy_url=proxy_url)

    def crawl(self, start_urls, depth=1):
        """
        Crawls a list of start_urls.
        For a production system, a queue-based approach (like Celery/Scrapy) is recommended.
        This provides a simple, robust implementation for demonstration.
        """
        results = []
        for url in start_urls:
            logging.info(f"Crawling: {url}")
            response = self.tor_session.get(url)
            
            if response and response.status_code == 200:
                results.append({
                    'url': url,
                    'html': response.text,
                    'status': response.status_code
                })
            else:
                logging.warning(f"Failed to crawl {url}. Status: {response.status_code if response else 'Timeout/Error'}")
                
        return results

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    spider = Spider()
    # Note: duckduckgo onion link for testing
    urls = ["http://duckduckgogg42xjoc72x3sjiqb85n2ihf68w1fngomr4m1h35p8o6ad.onion"]
    crawled_data = spider.crawl(urls)
    print(f"Crawled {len(crawled_data)} pages.")
