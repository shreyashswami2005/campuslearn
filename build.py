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
