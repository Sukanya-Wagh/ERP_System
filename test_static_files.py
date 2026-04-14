#!/usr/bin/env python3
"""
Test if static files are being served correctly by Flask
"""

from app import app
import os

def test_static_files():
    print("=== STATIC FILES TEST ===\n")
    
    # Check if static folder exists
    static_folder = app.static_folder
    print(f"Static folder path: {static_folder}")
    print(f"Static folder exists: {os.path.exists(static_folder)}")
    
    if os.path.exists(static_folder):
        print(f"Static folder contents: {os.listdir(static_folder)}")
    
    # Check if logo file exists
    logo_path = os.path.join(static_folder, 'sveri.png')
    print(f"\nLogo file path: {logo_path}")
    print(f"Logo file exists: {os.path.exists(logo_path)}")
    
    if os.path.exists(logo_path):
        file_size = os.path.getsize(logo_path)
        print(f"Logo file size: {file_size} bytes ({file_size/1024:.1f} KB)")
    
    # Test Flask static URL generation
    with app.app_context():
        logo_url = app.url_for('static', filename='sveri.png')
        print(f"\nFlask generated logo URL: {logo_url}")
    
    print("\n=== POSSIBLE ISSUES ===")
    print("1. If using deployment server (like Gunicorn), static files might not be served")
    print("2. Web server (Nginx/Apache) might not be configured to serve static files")
    print("3. File permissions might be incorrect")
    print("4. Static folder might not be in the deployment package")
    
    print("\n=== SOLUTIONS ===")
    print("1. For development: Use 'python app.py' to serve static files")
    print("2. For production: Configure web server to serve static files")
    print("3. Check if static folder is included in deployment files")
    print("4. Verify file permissions on static folder and files")

if __name__ == "__main__":
    test_static_files()
