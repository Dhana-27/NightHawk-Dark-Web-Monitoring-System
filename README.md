# Dark Web Threat Intelligence System

A full-stack cybersecurity research toolkit designed to passively collect, process, analyze, and visualize data from anonymized networks safely and ethically.

## Features

- **TOR Crawler:** Uses `requests` with SOCKS5 proxy to navigate `.onion` domains safely.
- **Data Processor:** Utilizes `BeautifulSoup` to clean HTML and regex to extract emails and crypto addresses. SHA-256 is used for duplicate removal.
- **Dual DB Storage:** `MongoDB` for raw crawl storage and `Elasticsearch` for fast analytical querying.
- **Analysis Engine:** Detects critical threat keywords and uses NLP (K-Means, TF-IDF) to cluster similar threats.
- **Alert App:** Mocks high severity alerts for suspicious activities.
- **Flask Dashboard:** A clean, responsive UI to visualize trends and metrics.

## Architecture

* **Backend:** Python
* **Data parsing:** BeautifulSoup4
* **Analytics:** Scikit-Learn
* **Storage:** MongoDB & Elasticsearch
* **Frontend:** Flask, HTML/CSS/JS, Chart.js

## Prerequisites

1.  **Python 3.8+**
2.  **MongoDB Server:** Running locally on default port `27017`.
3.  **Elasticsearch Server:** Running locally on default port `9200`.
4.  **TOR Service:** Ensure TOR proxy is running on `127.0.0.1:9050`.

## Installation

1.  Navigate to the project directory:
    ```bash
    cd c:\Users\DHANALAKSHMI\OneDrive\Documents\TOR
    ```

2.  Create and activate a virtual environment (Optional but Recommended):
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

### 1. Run the Main Pipeline (Demo Mode)
This simulates crawling some dark web sites and feeds mock data into the processing and analysis pipeline.
```bash
python main.py --demo
```

### 2. Start the Dashboard UI
Start the Flask application to view visually the data (using mock backend API logic for demonstration).
```bash
python web/app.py
```
Then navigate to `http://127.0.0.1:5000` in your web browser.

## Important Note on Ethics

This tool is designed strictly for passive, ethical **Threat Intelligence Research**.
- Do **NOT** attempt to deanonymize users.
- Do **NOT** participate in or facilitate illegal activities.
- Maintain a proper proxy separation when interacting with live Tor nodes.
