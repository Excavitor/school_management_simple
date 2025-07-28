#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

User = get_user_model()

def check_groups():
    print("Checking groups and permissions...")
    
    for group in Group.objects.all():
        print(f"\n📋 Group: {group.name}")
        print(f"   Users: {group.user_set.count()}")
        print(f"   Permissions: {group.permissions.count()}")
        for perm in group.permissions.all():
            print(f"     - {perm.codename} ({perm.name})")
    
    print(f"\n👥 Users and their groups:")
    for user in User.objects.all():
        groups = list(user.groups.all())
        print(f"   {user.email}: {[g.name for g in groups]}")

if __name__ == '__main__':
    check_groups()