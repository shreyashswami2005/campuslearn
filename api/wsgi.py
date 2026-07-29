import os
from django.core.wsgi import get_wsgi_application
from vercel_wsgi import handler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_wsgi_application()
handler = handler(application)
