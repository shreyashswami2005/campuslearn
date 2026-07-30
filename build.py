"""Run database migrations during Vercel build."""

import os
import sys

from dotenv import load_dotenv


def main():
    load_dotenv('.env.local')
    load_dotenv('.env')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    import django
    from django.core.management import call_command

    django.setup()
    print('Running migrate...')
    call_command('migrate', interactive=False, verbosity=1)
    
    # Auto-create / update production superuser
    try:
        from django.contrib.auth import get_user_model
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
            print('Production superuser "admin" created/updated.')
    except Exception as e:
        print(f'Warning: Could not create superuser: {e}')

    print('Build migrations complete.')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        # Allow first deploy before DATABASE_URL is set; fail loudly otherwise
        if not os.environ.get('DATABASE_URL'):
            print('Skipping migrate (no DATABASE_URL).', file=sys.stderr)
            sys.exit(0)
        print(f'Migrate failed: {exc}', file=sys.stderr)
        sys.exit(1)
