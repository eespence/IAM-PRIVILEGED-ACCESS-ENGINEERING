import datetime
import os

SPLUNK_HOME = os.environ.get("SPLUNK_HOME", "/opt/splunk")
LOG_FILE = f"{SPLUNK_HOME}/var/log/splunk/iam_alert_log.txt"

def log_event(event_type, action):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(f"{datetime.datetime.now()} | {event_type} | {action}\n")
    except Exception as e:
        print(f"ERROR: {e}")

def handle_event(event_type):
    if event_type == "FAILED_LOGIN":
        log_event(event_type, "Simulated account lockout triggered")
    elif event_type == "VAULT_ACCESS":
        log_event(event_type, "Sensitive credential access logged")
    elif event_type == "PRIVILEGED_LOGIN":
        log_event(event_type, "Privileged session flagged for review")
    else:
        log_event(event_type, "Unknown event type")

if __name__ == "__main__":
    # Hardcoded due to Splunk 9.2 alert action limitations
    handle_event("VAULT_ACCESS")