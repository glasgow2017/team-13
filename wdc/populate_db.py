import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'wdc.settings')
django.setup()

from django.contrib.auth.models import User

from wdc_main.models import Request, Call, UserProfile


def create_users():
    admin = User(username='Admin')
    admin.set_password('Admin')
    admin.is_superuser = True
    admin.is_staff = True
    admin.save()
    admin_profile = UserProfile(name='Admin', role=2)
    admin_profile.user = admin
    admin_profile.save()

if __name__ == '__main__':
    print("Creating users...")
    create_users()
    print("Users created successfully.")