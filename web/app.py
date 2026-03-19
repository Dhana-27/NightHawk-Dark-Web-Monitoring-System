from flask import Flask, render_template, jsonify
# from storage.es_client import ESStorage
# from storage.mongo_client import MongoStorage
import random
import datetime

app = Flask(__name__)

# Mock data for demonstration when DB is not populated
def get_mock_stats():
    return {
        "total_crawled": random.randint(1000, 5000),
        "threats_detected": random.randint(50, 200),
        "active_alerts": random.randint(1, 10),
        "recent_alerts": [
            {"time": "10:30 AM", "type": "Credentials Leak", "domain": "onionfiledump..."},
            {"time": "09:15 AM", "type": "Exploit mentioned", "domain": "0daymarket..."},
            {"time": "08:00 AM", "type": "Credit cards", "domain": "ccstorehouse..."}
        ],
        "top_keywords": [
            {"keyword": "leak", "count": random.randint(100, 300)},
            {"keyword": "exploit", "count": random.randint(50, 150)},
            {"keyword": "password", "count": random.randint(200, 400)},
            {"keyword": "hack", "count": random.randint(50, 100)}
        ]
    }

@app.route('/')
def dashboard():
    """
    Renders the main dashboard page.
    """
    return render_template('dashboard.html')

@app.route('/api/stats')
def api_stats():
    """
    Returns statistics for the dashboard charts and counters in JSON.
    In a real app, this would query Elasticsearch and MongoDB.
    """
    # For a real implementation:
    # es = ESStorage()
    # stats = es.get_aggregate_stats()
    stats = get_mock_stats()
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
