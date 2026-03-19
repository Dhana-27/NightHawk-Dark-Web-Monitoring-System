import argparse
import logging
import random
from crawler.spider import Spider
from processor.html_parser import HtmlParser
from processor.deduplicator import Deduplicator
from storage.mongo_client import MongoStorage
from storage.es_client import ESStorage
from analyzer.keyword_scanner import KeywordScanner
from analyzer.nlp_clustering import NLPClusterer
from alerts.notifier import Notifier

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_demo():
    """
    Simulates a crawl operation, processes data, stores it, and triggers analysis.
    Normally, this would run continually in a background worker (like Celery).
    """
    logging.info("Starting Dark Web Threat Intel System Pipeline")
    
    # Initialize components
    # Note: To fully work, MongoDB, ES and Tor proxy need to be running. 
    # For demo purposes, we will mock the crawling if the proxy fails.
    
    spider = Spider()
    parser = HtmlParser()
    dedup = Deduplicator()
    mongo = MongoStorage()
    es = ESStorage()
    scanner = KeywordScanner()
    nlp = NLPClusterer(num_clusters=2)
    notifier = Notifier()

    # 1. Crawl Phase
    logging.info("--- Phase 1: Crawling ---")
    urls_to_crawl = [
        "http://dummy1.onion",
        "http://dummy2.onion",
        "http://dummy3.onion"
    ]
    
    # Simulating crawls since dummy links won't resolve
    crawled_data = []
    for url in urls_to_crawl:
        # Here we mock the HTML response. In reality: result = spider.crawl([url])
        mock_html = f"<html><title>Dark Market {url}</title><body>We have new leaks and exploits available. Buy with BTC: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa. Contact admin_{random.randint(10,99)}@example.com</body></html>"
        crawled_data.append({"url": url, "html": mock_html})
        logging.info(f"Crawled: {url}")

    processed_docs = []

    # 2. Processing Phase
    logging.info("--- Phase 2: Processing ---")
    for data in crawled_data:
        parsed = parser.parse(data['html'])
        content_hash = dedup.generate_hash(parsed['text'])
        
        doc = {
            "url": data['url'],
            "content_hash": content_hash,
            "title": parsed['title'],
            "text": parsed['text'],
            "emails": parsed['emails'],
            "crypto_addresses": parsed['crypto_addresses'],
            "html_snapshot": data['html']
        }
        processed_docs.append(doc)
        logging.info(f"Parsed {data['url']} - Extracted {len(parsed['emails'])} emails and {len(parsed['crypto_addresses'])} crypto addresses.")

    # 3. Storage Phase
    logging.info("--- Phase 3: Storage ---")
    nlp_corpus = []
    stored_count = 0
    for doc in processed_docs:
        # In a real run, this inserts into MongoDB
        is_new = mongo.insert_document(doc)
        
        # We index into ES regardless of MongoDB for demo purposes, 
        # normally we only index if it's new
        es.index_document(doc['content_hash'], {
            "url": doc['url'],
            "title": doc['title'],
            "text": doc['text'],
            "timestamp": "2024-05-24T12:00:00Z", # Demo timestamp
            "emails": doc['emails'],
            "crypto_addresses": doc['crypto_addresses']
        })
        
        nlp_corpus.append(doc['text'])
        stored_count += 1
        
    logging.info(f"Stored {stored_count} documents.")

    # 4. Analysis & Alerts Phase
    logging.info("--- Phase 4: Analysis & Alerting ---")
    for doc in processed_docs:
        flags = scanner.scan(doc['text'])
        if list(set(['leak', 'exploit', 'credentials']).intersection(set(flags))):
            notifier.alert("Threat Detected", f"High priority keywords {flags} found at {doc['url']}", severity="CRITICAL")

    logging.info("Running NLP Clustering on gathered data...")
    if len(nlp_corpus) >= 2:
        labels = nlp.cluster_documents(nlp_corpus)
        logging.info(f"Clustering map: {list(zip([d['url'] for d in processed_docs], labels))}")
        top_terms = nlp.get_top_terms_per_cluster(3)
        for cluster, terms in top_terms.items():
            logging.info(f"{cluster} top terms: {terms}")

    logging.info("Pipeline Execution Complete. Review Dashboard for updates.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dark Web Threat Intel System Orchestrator")
    parser.add_argument("--demo", action="store_true", help="Run a demo pipeline with simulated data")
    
    args = parser.parse_args()
    
    if args.demo:
        run_demo()
    else:
        print("Please run with --demo to execute the mock pipeline, or implement a Celery task queue for production.")
