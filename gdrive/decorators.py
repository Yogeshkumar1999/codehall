from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        print(request.user.is_authenticated)
        if request.user.is_authenticated:
            return redirect('user')
        else:
            return view_func(request, *args, *kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            print('working', allowed_roles)
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            return HttpResponse('You are Not auth to see this page')
        return wrapper_func
    return decorator



def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return redirect('user')

        if group == 'admin':
            return view_func(request, *args, **kwargs)
    return wrapper_func

