"""
Custom worker class for serving media files in production (Render).
"""
import os
import mimetypes
from django.conf import settings


class MediaServeWorker:
    """
    Custom worker that serves media files in production.
    """
    
    def __init__(self, application):
        self.application = application
        # Register additional MIME types
        if not settings.DEBUG:
            mimetypes.add_type('image/jpeg', '.jpg', strict=False)
            mimetypes.add_type('image/jpeg', '.jpeg', strict=False)
            mimetypes.add_type('image/png', '.png', strict=False)
            mimetypes.add_type('image/gif', '.gif', strict=False)
            mimetypes.add_type('image/webp', '.webp', strict=False)
            mimetypes.add_type('image/svg+xml', '.svg', strict=False)
            mimetypes.add_type('video/mp4', '.mp4', strict=False)
            mimetypes.add_type('video/webm', '.webm', strict=False)
            mimetypes.add_type('video/ogg', '.ogg', strict=False)
            mimetypes.add_type('audio/mpeg', '.mp3', strict=False)
            mimetypes.add_type('audio/wav', '.wav', strict=False)
    
    def __call__(self, environ, start_response):
        """
        Serve media files directly from disk.
        """
        # Check if the request is for a media file
        path_info = environ.get('PATH_INFO', '')
        
        if path_info.startswith(settings.MEDIA_URL):
            # Serve media file directly
            media_file_path = os.path.join(settings.MEDIA_ROOT, path_info[len(settings.MEDIA_URL):])
            
            if os.path.exists(media_file_path) and os.path.isfile(media_file_path):
                # Get file size
                file_size = os.path.getsize(media_file_path)
                
                # Get content type
                content_type, _ = mimetypes.guess_type(media_file_path)
                if content_type is None:
                    content_type = 'application/octet-stream'
                
                # Read file content
                with open(media_file_path, 'rb') as f:
                    file_content = f.read()
                
                # Send response
                status = '200 OK'
                headers = [
                    ('Content-Type', content_type),
                    ('Content-Length', str(file_size)),
                ]
                start_response(status, headers)
                return [file_content]
        
        # For all other requests, use Django's WSGI application
        return self.application(environ, start_response)
