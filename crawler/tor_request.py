import requests
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class TorSession:
    def __init__(self, proxy_url="socks5h://127.0.0.1:9050", retries=3, backoff_factor=0.3):
        """
        Initializes a requests Session routed through a SOCKS5 proxy (Tor).
        """
        self.session = requests.Session()
        
        # Configure proxy
        self.session.proxies = {
            'http': proxy_url,
            'https': proxy_url
        }

        # Configure retry logic
        retry_strategy = Retry(
            total=retries,
            status_forcelist=[429, 500, 502, 503, 504],
            backoff_factor=backoff_factor,
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Add a default User-Agent to avoid basic blocking
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0'
        })
        
        logging.info(f"TorSession initialized with proxy: {proxy_url}")

    def get(self, url, timeout=15, **kwargs):
        """
        Performs a GET request using the Tor session.
        """
        try:
            response = self.session.get(url, timeout=timeout, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching {url}: {e}")
            return None

    def check_ip(self):
        """
        Helper method to verify if the traffic is being routed through Tor.
        """
        try:
            res = self.get("http://httpbin.org/ip")
            if res:
                return res.json()
        except Exception as e:
            logging.error(f"Failed to check IP: {e}")
            return None

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ts = TorSession()
    ip_info = ts.check_ip()
    print("Current IP Info (Should be Tor Node):", ip_info)
