from django.core.exceptions import PermissionDenied
from functools import wraps

def role_required(*roles):
    """
    Декоратор для ограничения доступа к view по ролям пользователя.
    Пример: @role_required('admin', 'manager')
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            user_profile = getattr(request.user, 'profile', None)
            if user_profile and user_profile.role and user_profile.role.name in roles:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return _wrapped_view
    return decorator 