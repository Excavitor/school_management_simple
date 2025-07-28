from django.contrib import admin
from .models import Notice, AdmissionApplication


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'content')
    list_editable = ('is_active',)
    ordering = ('-created_at',)


@admin.register(AdmissionApplication)
class AdmissionApplicationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'grade_applying_for', 'created_at')
    list_filter = ('grade_applying_for', 'gender', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'parent_name')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Student Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'gender', 'address', 'previous_school', 'grade_applying_for')
        }),
        ('Parent/Guardian Information', {
            'fields': ('parent_name', 'parent_phone', 'parent_email')
        }),
        ('Application Details', {
            'fields': ('created_at',)
        }),
    )
