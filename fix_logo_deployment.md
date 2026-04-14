# Logo Display Fix for Deployed Website

## Problem
Logo (sveri.png) is not displaying on deployed website, showing broken image icon.

## Root Cause
Deployment servers (like Heroku, PythonAnywhere, etc.) often don't serve static files automatically. Flask serves static files in development mode, but not in production.

## Solutions

### Solution 1: Use Absolute URL (Quick Fix)
Replace the logo path in login.html with an absolute URL:

```html
<!-- OLD -->
<img src="{{ url_for('static', filename='sveri.png') }}" alt="College Logo">

<!-- NEW - Use absolute URL -->
<img src="https://your-domain.com/static/sveri.png" alt="College Logo">
```

### Solution 2: Configure Web Server (Production)
If using Nginx/Apache, configure static file serving:

**Nginx Configuration:**
```nginx
location /static {
    alias /path/to/your/app/static;
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

**Apache Configuration:**
```apache
Alias /static /path/to/your/app/static
<Directory /path/to/your/app/static>
    Require all granted
</Directory>
```

### Solution 3: Use Cloud Storage
Upload logo to cloud service and use CDN URL:

```html
<img src="https://i.imgur.com/YOUR_LOGO_ID.png" alt="College Logo">
```

### Solution 4: Inline Base64 (Small Files)
Convert logo to base64 and embed directly:

```html
<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..." alt="College Logo">
```

## Testing Steps

1. **Check if static folder is deployed**
   - Verify static folder exists on server
   - Check file permissions (755 for folder, 644 for files)

2. **Test static URL directly**
   - Open: `https://your-domain.com/static/sveri.png`
   - Should show the logo image

3. **Check server logs**
   - Look for 404 errors for static files
   - Check if static requests are reaching the server

## Quick Fix Implementation

I'll update the login.html to use a more reliable approach:

```html
<!-- Multiple fallback options -->
<img src="{{ url_for('static', filename='sveri.png') }}" 
     onerror="this.src='https://i.imgur.com/LOGO_BACKUP.png'"
     alt="College Logo" 
     class="img-fluid" 
     style="height: 100%; width: 100%; object-fit: contain;">
```

## Deployment Checklist

- [ ] Static folder included in deployment package
- [ ] Web server configured for static files
- [ ] File permissions set correctly
- [ ] Logo file exists and is accessible
- [ ] SSL certificate installed (if using HTTPS)

## Contact Support

If issue persists, provide:
1. Deployment platform (Heroku, PythonAnywhere, etc.)
2. Web server being used (Nginx, Apache, etc.)
3. URL of your deployed website
4. Error messages from browser console
