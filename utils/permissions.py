import os
from dotenv import load_dotenv

load_dotenv()

def is_admin(user_id):
    """Check if user is admin"""
    admin_ids_str = os.getenv('ADMIN_ID', '')
    
    # Support multiple admin IDs separated by commas
    admin_ids = [int(id.strip()) for id in admin_ids_str.split(',') if id.strip()]
    
    return user_id in admin_ids