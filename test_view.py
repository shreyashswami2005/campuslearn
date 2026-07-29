import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from django.test import Client
c = Client()
# Create a test user
from django.contrib.auth.models import User
User.objects.create_user(username='testuser', password='testpass')
# Login
c.login(username='testuser', password='testpass')
response = c.get('/dashboard/')
print('Status code:', response.status_code)
print('Content snippet:', response.content[:200])
