import hashlib

class Deduplicator:
    def __init__(self):
        pass

    def generate_hash(self, text_content):
        """
        Generates a SHA-256 hash for the given text content to be used for deduplication.
        """
        if not text_content:
            return None
        
        hasher = hashlib.sha256()
        hasher.update(text_content.encode('utf-8'))
        return hasher.hexdigest()

if __name__ == "__main__":
    dedup = Deduplicator()
    hash1 = dedup.generate_hash("Hello World")
    hash2 = dedup.generate_hash("Hello World")
    hash3 = dedup.generate_hash("Hello Dark Web")
    
    print(f"Hash 1: {hash1}")
    print(f"Hash 2: {hash2}")
    print(f"Hash 3: {hash3}")
    print(f"Match 1 & 2: {hash1 == hash2}")
