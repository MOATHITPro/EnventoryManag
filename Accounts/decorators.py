from django.core.exceptions import PermissionDenied

def manager_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.user_type == 'manager':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap

def operator_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.user_type == 'operator':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap
