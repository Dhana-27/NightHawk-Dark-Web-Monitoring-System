from pymongo import MongoClient
import logging
import datetime

class MongoStorage:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="threat_intel"):
        """
        Initializes MongoDB connection.
        Make sure MongoDB is running locally or provide a remote URI.
        """
        try:
            self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            self.db = self.client[db_name]
            self.collection = self.db['raw_crawls']
            
            # Create indexing for faster queries
            self.collection.create_index("content_hash", unique=True)
            self.collection.create_index("url")
            
            logging.info(f"Connected to MongoDB: {db_name}")
        except Exception as e:
            logging.error(f"Failed to connect to MongoDB: {e}")

    def insert_document(self, data):
        """
        Inserts a documented into the raw_crawls collection.
        Expects a dict with: url, content_hash, html, parsed_text, timestamp, etc.
        """
        try:
            # Check if hash already exists
            if self.collection.find_one({"content_hash": data.get("content_hash")}):
                logging.info(f"Duplicate content found for hash: {data.get('content_hash')}. Skipping insert.")
                return False
                
            data['timestamp'] = datetime.datetime.utcnow()
            result = self.collection.insert_one(data)
            logging.info(f"Document inserted with ID: {result.inserted_id}")
            return True
        except Exception as e:
            logging.error(f"Error inserting document: {e}")
            return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    mongo = MongoStorage()
    sample_data = {
        "url": "http://example.onion",
        "content_hash": "dummyhash12345",
        "html": "<html><body>test</body></html>",
        "parsed_text": "test"
    }
    mongo.insert_document(sample_data)
