from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError
import logging

class ESStorage:
    def __init__(self, hosts=["http://localhost:9200"], index_name="threat_data"):
        """
        Initializes Elasticsearch connection.
        """
        self.index_name = index_name
        try:
            self.es = Elasticsearch(hosts)
            if not self.es.ping():
                logging.error("Elasticsearch ping failed. Is the server running?")
            else:
                logging.info(f"Connected to Elasticsearch")
                self._create_index()
        except Exception as e:
            logging.error(f"Failed to connect to Elasticsearch: {e}")

    def _create_index(self):
        """
        Creates an index with specific mappings if it doesn't exist.
        """
        mapping = {
            "mappings": {
                "properties": {
                    "url": {"type": "keyword"},
                    "title": {"type": "text"},
                    "text": {"type": "text"},
                    "emails": {"type": "keyword"},
                    "crypto_addresses": {"type": "keyword"},
                    "timestamp": {"type": "date"},
                    "flags": {"type": "keyword"} # threat alerts like 'leak', 'exploit'
                }
            }
        }
        
        try:
            if not self.es.indices.exists(index=self.index_name):
                self.es.indices.create(index=self.index_name, body=mapping)
                logging.info(f"Index '{self.index_name}' created.")
            else:
                logging.info(f"Index '{self.index_name}' already exists.")
        except Exception as e:
            logging.error(f"Error creating index: {e}")

    def index_document(self, doc_id, data):
        """
        Indexes a document for quick search and analysis.
        doc_id could be the content_hash from MongoDB.
        """
        try:
            res = self.es.index(index=self.index_name, id=doc_id, document=data)
            logging.info(f"Document indexed in ES: {res['result']}")
            return res['result'] == 'created'
        except Exception as e:
            logging.error(f"Error indexing document: {e}")
            return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    es = ESStorage()
