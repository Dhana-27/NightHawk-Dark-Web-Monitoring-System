class KeywordScanner:
    def __init__(self, keywords=None):
        if keywords is None:
            # Default threat intelligence keywords
            self.keywords = ['leak', 'exploit', 'credentials', 'password', 'hack', 'vulnerability', 'cve', 'weapon']
        else:
            self.keywords = keywords

    def scan(self, text_content):
        """
        Scans text for threat-related keywords.
        Returns a list of matched keywords to act as 'flags' or tags.
        """
        matches = []
        if not text_content:
            return matches
            
        text_lower = text_content.lower()
        for kw in self.keywords:
            if kw in text_lower:
                matches.append(kw)
        
        return list(set(matches))

if __name__ == "__main__":
    scanner = KeywordScanner()
    sample_text = "We have a new 0-day exploit for sale. Grab the leaked credentials here."
    flags = scanner.scan(sample_text)
    print(f"Keywords found: {flags}")
