import json
import os

SHORTENERS_FILE = 'shorteners.json'

def load_shorteners():
    """Load shorteners from JSON file"""
    if not os.path.exists(SHORTENERS_FILE):
        return []
    
    try:
        with open(SHORTENERS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_shorteners(shorteners):
    """Save shorteners to JSON file"""
    try:
        with open(SHORTENERS_FILE, 'w') as f:
            json.dump(shorteners, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving shorteners: {e}")
        return False

def add_shortener(name, base, api_key):
    """Add a new shortener"""
    shorteners = load_shorteners()
    
    new_shortener = {
        "name": name,
        "base": base,
        "api": api_key,
        "status": "active"
    }
    
    shorteners.append(new_shortener)
    return save_shorteners(shorteners)

def list_shorteners():
    """List all shorteners"""
    shorteners = load_shorteners()
    
    if not shorteners:
        return "📜 No shorteners configured yet.\nUse /addshort to add one."
    
    result = "📜 **Shorteners List:**\n\n"
    for i, shortener in enumerate(shorteners, 1):
        status = "Active" if shortener['status'] == 'active' else "Paused"
        result += f"{i}️⃣ {shortener['name']} ({status})\n"
    
    return result

def toggle_shortener(index):
    """Toggle shortener status between active and paused"""
    shorteners = load_shorteners()
    
    if index < 0 or index >= len(shorteners):
        return "⚠️ Invalid shortener index."
    
    current_status = shorteners[index]['status']
    new_status = 'paused' if current_status == 'active' else 'active'
    shorteners[index]['status'] = new_status
    
    if save_shorteners(shorteners):
        status_text = "Paused" if new_status == 'paused' else "Resumed"
        return f"✅ Shortener '{shorteners[index]['name']}' {status_text}."
    else:
        return "⚠️ Failed to update shortener status."

def remove_shortener(index):
    """Remove a shortener"""
    shorteners = load_shorteners()
    
    if index < 0 or index >= len(shorteners):
        return "⚠️ Invalid shortener index."
    
    removed_name = shorteners[index]['name']
    shorteners.pop(index)
    
    if save_shorteners(shorteners):
        return f"✅ Shortener '{removed_name}' removed successfully."
    else:
        return "⚠️ Failed to remove shortener."

def get_active_shorteners():
    """Get list of active shorteners"""
    shorteners = load_shorteners()
    return [s for s in shorteners if s['status'] == 'active']