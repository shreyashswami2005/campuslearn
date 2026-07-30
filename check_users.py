import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Ensure 'admin' superuser exists
admin_user, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com'})
admin_user.set_password('admin123')
admin_user.is_staff = True
admin_user.is_superuser = True
admin_user.save()
print("ADMIN CREATED/UPDATED: admin / admin123")
