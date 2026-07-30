import os
from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_wsgi_application()

try:
    from django.core.management import call_command
    from django.contrib.auth import get_user_model

    call_command('migrate', interactive=False)

    User = get_user_model()
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@college.com',
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
        }
    )
    if created or not admin_user.check_password('admin123'):
        admin_user.set_password('admin123')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.is_active = True
        admin_user.save()
        print("Production superuser 'admin' verified.")
except Exception as e:
    print("Auto-setup on cold start warning:", e)
