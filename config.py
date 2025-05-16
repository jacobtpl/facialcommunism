import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    UPLOAD_FOLDER = os.path.join('app', 'images')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB limit for uploads
