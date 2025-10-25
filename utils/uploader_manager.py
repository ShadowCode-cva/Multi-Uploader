import json
import os

UPLOADS_FILE = 'uploads.json'

def load_uploaders():
    """Load uploaders from JSON file"""
    if not os.path.exists(UPLOADS_FILE):
        return []
    
    try:
        with open(UPLOADS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_uploaders(uploaders):
    """Save uploaders to JSON file"""
    try:
        with open(UPLOADS_FILE, 'w') as f:
            json.dump(uploaders, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving uploaders: {e}")
        return False

def add_uploader(name, endpoint, api_key):
    """Add a new uploader"""
    uploaders = load_uploaders()
    
    new_uploader = {
        "name": name,
        "endpoint": endpoint,
        "api": api_key,
        "status": "active"
    }
    
    uploaders.append(new_uploader)
    return save_uploaders(uploaders)

def list_uploaders():
    """List all uploaders"""
    uploaders = load_uploaders()
    
    if not uploaders:
        return "🗂️ No uploaders configured yet.\nUse /addupload to add one."
    
    result = "🗂️ **Uploaders List:**\n\n"
    for i, uploader in enumerate(uploaders, 1):
        status = "Active" if uploader['status'] == 'active' else "Paused"
        result += f"{i}️⃣ {uploader['name']} ({status})\n"
    
    return result

def toggle_uploader(index):
    """Toggle uploader status between active and paused"""
    uploaders = load_uploaders()
    
    if index < 0 or index >= len(uploaders):
        return "⚠️ Invalid uploader index."
    
    current_status = uploaders[index]['status']
    new_status = 'paused' if current_status == 'active' else 'active'
    uploaders[index]['status'] = new_status
    
    if save_uploaders(uploaders):
        status_text = "Paused" if new_status == 'paused' else "Resumed"
        return f"✅ Uploader '{uploaders[index]['name']}' {status_text}."
    else:
        return "⚠️ Failed to update uploader status."

def remove_uploader(index):
    """Remove an uploader"""
    uploaders = load_uploaders()
    
    if index < 0 or index >= len(uploaders):
        return "⚠️ Invalid uploader index."
    
    removed_name = uploaders[index]['name']
    uploaders.pop(index)
    
    if save_uploaders(uploaders):
        return f"✅ Uploader '{removed_name}' removed successfully."
    else:
        return "⚠️ Failed to remove uploader."

def get_active_uploaders():
    """Get list of active uploaders"""
    uploaders = load_uploaders()
    return [u for u in uploaders if u['status'] == 'active']