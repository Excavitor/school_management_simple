from django.db import models


class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        permissions = [
            ('can_manage_notices', 'Can manage notices'),
        ]
    
    def __str__(self):
        return self.title


class AdmissionApplication(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField()
    previous_school = models.CharField(max_length=200, blank=True)
    grade_applying_for = models.CharField(max_length=20)
    parent_name = models.CharField(max_length=100)
    parent_phone = models.CharField(max_length=15)
    parent_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        permissions = [
            ('can_manage_admissions', 'Can manage admission applications'),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.grade_applying_for}"
