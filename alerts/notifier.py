import logging

class Notifier:
    def __init__(self, webhook_url=None, email_config=None):
        self.webhook_url = webhook_url
        self.email_config = email_config

    def alert(self, subject, message, severity="INFO"):
        """
        Logs the alert. In a production scenario, this method would
        dispatch to a Discord webhook, Slack, or send an Email via SMPT.
        """
        alert_msg = f"[{severity}] {subject} - {message}"
        logging.warning(f"ALERT TRIGGERED: {alert_msg}")
        
        if self.webhook_url:
            # e.g., requests.post(self.webhook_url, json={"text": alert_msg})
            pass

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    notifier = Notifier()
    notifier.alert("High Threat Detected", "Found exploit keyword in new onion site.", severity="CRITICAL")
