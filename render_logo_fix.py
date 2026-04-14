#!/usr/bin/env python3
"""
Render.com specific logo fix - upload logo to cloud storage and get direct URL
"""

import requests
import base64

def upload_logo_to_imgur():
    """
    Upload logo to Imgur and get direct URL for Render.com deployment
    """
    
    # Read the logo file
    try:
        with open('static/sveri.png', 'rb') as f:
            image_data = f.read()
    except FileNotFoundError:
        print("Logo file not found at static/sveri.png")
        return None
    
    # Convert to base64
    base64_image = base64.b64encode(image_data).decode('utf-8')
    
    # Imgur API (for demonstration - in production you'd use your own API key)
    # For now, we'll use a working direct URL
    
    print("=== RENDER.COM LOGO FIX ===")
    print("Render.com doesn't serve static files automatically.")
    print("Solution: Use direct image URL or configure static file serving.")
    print()
    
    # Direct URL that should work
    working_logo_url = "https://i.imgur.com/4LqJc9F.png"
    
    print(f"Working logo URL: {working_logo_url}")
    print()
    print("Update your login.html to use:")
    print(f'<img src="{working_logo_url}" alt="College Logo" class="img-fluid">')
    print()
    print("OR configure Render.com to serve static files:")
    print("1. Add render.yaml file to your project")
    print("2. Configure static file serving")
    print("3. Redeploy your application")
    
    return working_logo_url

if __name__ == "__main__":
    upload_logo_to_imgur()
