"""
Utility functions for the public app to reduce code duplication
"""
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response


def apply_search_filter(queryset, search_term, search_fields):
    """
    Apply search filter to queryset using provided fields
    
    Args:
        queryset: Django QuerySet to filter
        search_term: Search term from request
        search_fields: List of field names to search in
    
    Returns:
        Filtered queryset
    """
    if not search_term:
        return queryset
    
    # Build Q objects for each field
    q_objects = Q()
    for field in search_fields:
        q_objects |= Q(**{f"{field}__icontains": search_term})
    
    return queryset.filter(q_objects)


def check_api_permission(user, permission):
    """
    Check if user has permission for API operations
    
    Args:
        user: Django User instance
        permission: Permission string (e.g., 'public.add_notice')
    
    Returns:
        Response object if permission denied, None if allowed
    """
    if not user.is_authenticated or not user.has_perm(permission):
        return Response(
            {'detail': f'You do not have permission to perform this action.'},
            status=status.HTTP_403_FORBIDDEN
        )
    return None


# Common search field configurations
NOTICE_SEARCH_FIELDS = ['title', 'content']
ADMISSION_SEARCH_FIELDS = ['first_name', 'last_name', 'email']
USER_SEARCH_FIELDS = ['first_name', 'last_name', 'email']