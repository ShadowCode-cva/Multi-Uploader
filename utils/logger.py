import json
import os
from datetime import datetime

LOGS_FILE = 'logs.json'

def load_logs():
    """Load logs from JSON file"""
    if not os.path.exists(LOGS_FILE):
        return []
    
    try:
        with open(LOGS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_logs(logs):
    """Save logs to JSON file"""
    try:
        with open(LOGS_FILE, 'w') as f:
            json.dump(logs, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving logs: {e}")
        return False

def log_upload(username, user_id, link):
    """Log an upload event"""
    logs = load_logs()
    
    log_entry = {
        "user": username,
        "user_id": user_id,
        "link": link,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    logs.append(log_entry)
    save_logs(logs)
