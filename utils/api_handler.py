import requests
import logging
from utils.shortener_manager import get_active_shorteners
from utils.uploader_manager import get_active_uploaders

logger = logging.getLogger(__name__)

def shorten_url(shortener, url):
    """Shorten a single URL using a shortener"""
    try:
        # Construct API URL
        api_url = f"{shortener['base']}{shortener['api']}&url={url}"
        
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Different shorteners may return data differently
        # Try common response formats
        if 'shortenedUrl' in data:
            return data['shortenedUrl']
        elif 'shorturl' in data:
            return data['shorturl']
        elif 'short_url' in data:
            return data['short_url']
        elif 'url' in data:
            return data['url']
        elif 'link' in data:
            return data['link']
        else:
            logger.warning(f"Unknown response format from {shortener['name']}: {data}")
            return None
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Shortener {shortener['name']} failed: {e}")
        return None
    except Exception as e:
        logger.error(f"Error shortening with {shortener['name']}: {e}")
        return None

def shorten_urls(url):
    """Shorten URL using all active shorteners"""
    shorteners = get_active_shorteners()
    
    if not shorteners:
        return []
    
    shortened_urls = []
    for shortener in shorteners:
        shortened = shorten_url(shortener, url)
        if shortened:
            shortened_urls.append(shortened)
    
    return shortened_urls

def upload_to_platform(uploader, file_url):
    """Upload a file to a specific platform"""
    try:
        # Prepare the request based on common API patterns
        # Most upload APIs accept either 'url' or 'link' parameter
        
        headers = {
            'Authorization': f"Bearer {uploader['api']}"
        }
        
        data = {
            'url': file_url,
            'api_key': uploader['api']
        }
        
        response = requests.post(
            uploader['endpoint'],
            headers=headers,
            data=data,
            timeout=30
        )
        
        response.raise_for_status()
        result = response.json()
        
        # Try common response formats
        if 'url' in result:
            return result['url']
        elif 'link' in result:
            return result['link']
        elif 'download_url' in result:
            return result['download_url']
        elif 'file_url' in result:
            return result['file_url']
        else:
            logger.warning(f"Unknown response format from {uploader['name']}: {result}")
            return None
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Upload to {uploader['name']} failed: {e}")
        return None
    except Exception as e:
        logger.error(f"Error uploading to {uploader['name']}: {e}")
        return None

def upload_to_platforms(file_url):
    """Upload file to all active platforms and shorten their URLs"""
    uploaders = get_active_uploaders()
    
    if not uploaders:
        return []
    
    results = []
    
    for uploader in uploaders:
        uploaded_url = upload_to_platform(uploader, file_url)
        
        if uploaded_url:
            # Shorten the uploaded URL
            shortened_urls = shorten_urls(uploaded_url)
            
            results.append({
                'platform': uploader['name'],
                'url': uploaded_url,
                'shortened': shortened_urls
            })
        else:
            logger.warning(f"Skipping {uploader['name']} - upload failed")
    
    return results