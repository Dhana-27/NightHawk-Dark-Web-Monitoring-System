from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import logging

class NLPClusterer:
    def __init__(self, num_clusters=3):
        self.num_clusters = num_clusters
        self.vectorizer = TfidfVectorizer(stop_words='english', max_df=0.8, min_df=2)
        self.kmeans = KMeans(n_clusters=self.num_clusters, random_state=42, n_init=10)

    def cluster_documents(self, documents):
        """
        Takes a list of document strings, computes TF-IDF, and runs KMeans clustering.
        Returns a list of cluster labels corresponding to the input documents.
        Requires at least 'num_clusters' documents.
        """
        if len(documents) < self.num_clusters:
            logging.warning("Not enough documents to cluster.")
            return [-1] * len(documents)

        try:
            X = self.vectorizer.fit_transform(documents)
            self.kmeans.fit(X)
            return self.kmeans.labels_.tolist()
        except Exception as e:
            logging.error(f"Error during clustering: {e}")
            return [-1] * len(documents)

    def get_top_terms_per_cluster(self, num_terms=5):
        """
        Returns the top terms for each cluster to understand what the cluster is about.
        """
        try:
            order_centroids = self.kmeans.cluster_centers_.argsort()[:, ::-1]
            terms = self.vectorizer.get_feature_names_out()
            cluster_terms = {}
            for i in range(self.num_clusters):
                top_terms = [terms[ind] for ind in order_centroids[i, :num_terms]]
                cluster_terms[f"Cluster {i}"] = top_terms
            return cluster_terms
        except Exception as e:
            logging.error(f"Error fetching top terms: {e}")
            return {}

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    docs = [
        "New credentials leak found on the dark web.",
        "Database dump of user passwords and emails.",
        "Buy cheap electronics and stolen cards here.",
        "Stolen credit cards and dumps for sale.",
        "Zero day exploit for Windows Server.",
        "Exploit available for CVE-2023-XYZ."
    ]
    clusterer = NLPClusterer(num_clusters=3)
    labels = clusterer.cluster_documents(docs)
    print("Labels:", labels)
    print("Top terms:", clusterer.get_top_terms_per_cluster())
