#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from public.models import Notice, AdmissionApplication
from datetime import date

User = get_user_model()

def create_sample_data():
    print("Creating sample data...")
    
    # Create superuser
    if not User.objects.filter(email='admin@school.com').exists():
        admin = User.objects.create_superuser(
            email='admin@school.com',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        print("✓ Created superuser: admin@school.com / admin123")
    
    # Create groups and permissions
    notice_ct = ContentType.objects.get_for_model(Notice)
    admission_ct = ContentType.objects.get_for_model(AdmissionApplication)
    user_ct = ContentType.objects.get_for_model(User)
    group_ct = ContentType.objects.get_for_model(Group)
    
    # Get permissions for each content type
    notice_permissions = Permission.objects.filter(content_type=notice_ct)
    admission_permissions = Permission.objects.filter(content_type=admission_ct)
    user_permissions = Permission.objects.filter(content_type=user_ct)
    group_permissions = Permission.objects.filter(content_type=group_ct)
    
    # Notice Manager Group
    notice_group, created = Group.objects.get_or_create(name='Notice Manager')
    if created:
        notice_group.permissions.set(notice_permissions)
        print("✓ Created Notice Manager group")
    
    # Admission Manager Group
    admission_group, created = Group.objects.get_or_create(name='Admission Manager')
    if created:
        admission_group.permissions.set(admission_permissions)
        print("✓ Created Admission Manager group")
    
    # Full Manager Group (both notices and admissions)
    full_group, created = Group.objects.get_or_create(name='Full Manager')
    if created:
        all_permissions = list(notice_permissions) + list(admission_permissions)
        full_group.permissions.set(all_permissions)
        print("✓ Created Full Manager group")
    
    # User Manager Group (can manage users)
    user_group, created = Group.objects.get_or_create(name='User Manager')
    if created or not user_group.permissions.exists():
        user_group.permissions.set(user_permissions)
        print("✓ Created/Updated User Manager group")
    
    # Role Manager Group (can manage roles using Group permissions)
    role_group, created = Group.objects.get_or_create(name='Role Manager')
    if created or not role_group.permissions.exists():
        role_group.permissions.set(group_permissions)
        print("✓ Created/Updated Role Manager group")
    
    # Super Manager Group (can manage both users and roles)
    super_group, created = Group.objects.get_or_create(name='Super Manager')
    if created or not super_group.permissions.exists():
        super_permissions = list(user_permissions) + list(group_permissions)
        super_group.permissions.set(super_permissions)
        print("✓ Created/Updated Super Manager group")
    
    # Create sample users
    users_data = [
        {
            'email': 'notice.manager@school.com',
            'password': 'password123',
            'first_name': 'Notice',
            'last_name': 'Manager',
            'groups': ['Notice Manager']
        },
        {
            'email': 'admission.manager@school.com',
            'password': 'password123',
            'first_name': 'Admission',
            'last_name': 'Manager',
            'groups': ['Admission Manager']
        },
        {
            'email': 'full.manager@school.com',
            'password': 'password123',
            'first_name': 'Full',
            'last_name': 'Manager',
            'groups': ['Full Manager']
        },
        {
            'email': 'user.manager@school.com',
            'password': 'password123',
            'first_name': 'User',
            'last_name': 'Manager',
            'groups': ['User Manager']
        },
        {
            'email': 'role.manager@school.com',
            'password': 'password123',
            'first_name': 'Role',
            'last_name': 'Manager',
            'groups': ['Role Manager']
        },
        {
            'email': 'super.manager@school.com',
            'password': 'password123',
            'first_name': 'Super',
            'last_name': 'Manager',
            'groups': ['Super Manager']
        },
        {
            'email': 'regular.user@school.com',
            'password': 'password123',
            'first_name': 'Regular',
            'last_name': 'User',
            'groups': []
        }
    ]
    
    for user_data in users_data:
        if not User.objects.filter(email=user_data['email']).exists():
            user = User.objects.create_user(
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )
            
            for group_name in user_data['groups']:
                group = Group.objects.get(name=group_name)
                user.groups.add(group)
            
            print(f"✓ Created user: {user_data['email']} / password123")
    
    # Create sample notices
    sample_notices = [
        {
            'title': 'Welcome to New Academic Year 2025',
            'content': 'We are excited to welcome all students to the new academic year. Classes will begin on February 1st, 2025. Please ensure all admission formalities are completed before the start date.',
            'is_active': True
        },
        {
            'title': 'Sports Day Event - March 15, 2025',
            'content': 'Our annual sports day will be held on March 15, 2025. All students are encouraged to participate in various sporting events. Registration forms are available at the school office.',
            'is_active': True
        },
        {
            'title': 'Parent-Teacher Meeting Schedule',
            'content': 'Parent-teacher meetings are scheduled for the last Saturday of every month. Please check with your class teacher for specific timings and appointment booking.',
            'is_active': True
        },
        {
            'title': 'Library Renovation Notice',
            'content': 'The school library will be under renovation from February 10-20, 2025. During this period, students can access books from the temporary library setup in Room 201.',
            'is_active': False
        }
    ]
    
    for notice_data in sample_notices:
        if not Notice.objects.filter(title=notice_data['title']).exists():
            Notice.objects.create(**notice_data)
            print(f"✓ Created notice: {notice_data['title']}")
    
    # Create sample admission applications
    sample_applications = [
        {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@email.com',
            'phone': '123-456-7890',
            'date_of_birth': date(2010, 5, 15),
            'gender': 'M',
            'address': '123 Main Street, City, State 12345',
            'previous_school': 'ABC Elementary School',
            'grade_applying_for': 'Grade 8',
            'parent_name': 'Jane Doe',
            'parent_phone': '123-456-7891',
            'parent_email': 'jane.doe@email.com'
        },
        {
            'first_name': 'Emily',
            'last_name': 'Smith',
            'email': 'emily.smith@email.com',
            'phone': '234-567-8901',
            'date_of_birth': date(2009, 8, 22),
            'gender': 'F',
            'address': '456 Oak Avenue, City, State 12345',
            'previous_school': 'XYZ Middle School',
            'grade_applying_for': 'Grade 9',
            'parent_name': 'Robert Smith',
            'parent_phone': '234-567-8902',
            'parent_email': 'robert.smith@email.com'
        },
        {
            'first_name': 'Michael',
            'last_name': 'Johnson',
            'email': 'michael.johnson@email.com',
            'phone': '345-678-9012',
            'date_of_birth': date(2011, 12, 3),
            'gender': 'M',
            'address': '789 Pine Road, City, State 12345',
            'previous_school': '',
            'grade_applying_for': 'Grade 7',
            'parent_name': 'Sarah Johnson',
            'parent_phone': '345-678-9013',
            'parent_email': 'sarah.johnson@email.com'
        }
    ]
    
    for app_data in sample_applications:
        if not AdmissionApplication.objects.filter(
            email=app_data['email']
        ).exists():
            AdmissionApplication.objects.create(**app_data)
            print(f"✓ Created admission application: {app_data['first_name']} {app_data['last_name']}")
    
    print("\n🎉 Sample data creation completed!")
    print("\nLogin credentials:")
    print("Superuser: admin@school.com / admin123")
    print("Notice Manager: notice.manager@school.com / password123")
    print("Admission Manager: admission.manager@school.com / password123")
    print("Full Manager: full.manager@school.com / password123")
    print("User Manager: user.manager@school.com / password123")
    print("Role Manager: role.manager@school.com / password123")
    print("Super Manager: super.manager@school.com / password123")
    print("Regular User: regular.user@school.com / password123")

if __name__ == '__main__':
    create_sample_data()