import json

def format_result(original_link, original_shortened, upload_results):
    """
    Format the final result in the specified format:
    
    Drive link - <drive_link>
    Drive Shortner Link - ["shortner1","shortner2"]
    
    File Press - <filepress_link>
    File Press Shortner Link - ["shortner1","shortner2"]
    """
    
    result = ""
    
    # Format original link section
    result += f"Drive link - {original_link}\n"
    
    if original_shortened:
        shortened_json = json.dumps(original_shortened)
        result += f"Drive Shortner Link - {shortened_json}\n"
    else:
        result += "Drive Shortner Link - []\n"
    
    result += "\n"
    
    # Format each upload platform section
    for upload in upload_results:
        platform_name = upload['platform']
        platform_url = upload['url']
        platform_shortened = upload['shortened']
        
        result += f"{platform_name} - {platform_url}\n"
        
        if platform_shortened:
            shortened_json = json.dumps(platform_shortened)
            result += f"{platform_name} Shortner Link - {shortened_json}\n"
        else:
            result += f"{platform_name} Shortner Link - []\n"
        
        result += "\n"
    
    return result.strip()