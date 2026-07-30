import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client

client = Client()
print("1. Logging into Django Admin with admin credentials...")
login_success = client.login(username='admin', password='admin123')
print("   Login successful?", login_success)

admin_urls = [
    '/admin/',
    '/admin/auth/user/',
    '/admin/auth/group/',
    '/admin/accounts/studentprofile/',
    '/admin/courses/course/',
    '/admin/courses/lesson/',
    '/admin/courses/enrollment/',
    '/admin/courses/result/',
    '/admin/courses/attendance/',
    '/admin/quizzes/quiz/',
    '/admin/quizzes/question/',
    '/admin/marks/component/',
    '/admin/certificates/certificate/',
]

print("\n2. Testing Admin Page Navigation Across Tabs/URLs:")
all_passed = True
for url in admin_urls:
    res = client.get(url, follow=False)
    status = res.status_code
    print(f"GET {url:<40} => Status: {status}")
    if status != 200:
        all_passed = False
        print(f"   --> FAILED on {url}: Status {status}")

print("\n3. Verifying Session Cookie Settings:")
session_cookie = client.cookies.get('sessionid')
if session_cookie:
    print("   Session Cookie Present:")
    print("     Value:", session_cookie.value)
    print("     Path:", session_cookie['path'])
    print("     SameSite:", session_cookie['samesite'])
    print("     Secure:", session_cookie['secure'])
else:
    print("   ERROR: Session cookie missing!")
    all_passed = False

if all_passed and login_success:
    print("\nSUCCESS: All Django admin session persistence tests passed (100% Status 200)!")
else:
    print("\nFAILURE: Admin session tests failed!")
