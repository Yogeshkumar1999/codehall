from django.shortcuts import render, redirect
from .models import *
# Create your views here.
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.conf import settings
from django.http import FileResponse

from .decorators import unauthenticated_user, allowed_users, admin_only
from .forms import AllFilesForm, FilesForm, CreateUserForm, CustomerForm
from .filters import UserFilter

import os


total_size = 0
@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid:
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for '+username)
            return redirect('login')
    context = {'form':form}
    print("ok1")
    return render(request, 'gdrive/register.html', context)


@unauthenticated_user
def loginPage(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user')
        else:
            messages.info(request, 'Username Or password is incorrect')
    return render(request, 'gdrive/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def home(request):
    return render(request, 'gdrive/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    print(request.user.customer.profile_pic.url)
    form = CustomerForm(instance = customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance = customer)
        if form.is_valid:
            form.save()

    context = {'form':form}
    return render(request, 'gdrive/account_settings.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def fileError(request):
    return render(request, 'gdrive/file_error.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def uploadFile(request):
    global total_size
    print(total_size)
    if total_size > 1000:
        return render(request, 'gdrive/storage_error.html')
    form = FilesForm()
    customer = request.user.customer
    if request.method == 'POST':
        form = FilesForm(request.POST, request.FILES)
        upload_file = request.FILES
        if form.is_valid:
            print(upload_file.keys())
            model_instance = form.save(commit = False)
            file_name = upload_file['file_name'].name
            current_file_size = upload_file['file_name'].size/1000000
            if (total_size + current_file_size) > 1000:
                return render(request, 'gdrive/storage_error.html')

            model_instance.name = file_name
            file_extension = os.path.splitext(file_name)[-1]
            accpeted_file_extensions = set(['.pdf', '.html', '.txt', '.doc', '.docx', '.csv'])
            if file_extension in accpeted_file_extensions:
                model_instance.customer = customer
                print(upload_file['file_name'].name)
                model_instance.save()
                return redirect('user')
            else:
                return redirect('file_error')

    context = {'form':form}
    return render(request, 'gdrive/upload_file.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    global total_size
    #files = UserFiles.objects.all().delete()
    files =  request.user.customer.userfiles_set.all()
    total_size = 0
    for _file in files:
        print(_file.file_name)
        path = settings.MEDIA_ROOT+ '/documents/' +  _file.name
        print(path)
        total_size += os.stat(path).st_size
        print(total_size)

    total_size /= 1000000
    total_size = round(total_size)
    myfilter = UserFilter(request.GET, queryset = files)
    if request.method == 'GET':
        files = myfilter.qs
    context = {'files': files, 'myfilter':myfilter, 'total_size':total_size, 'progress': total_size/10}
    return render(request, 'gdrive/user.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def downloadFile(request, pk):
    _file = UserFiles.objects.get(id=pk)
    if request.method == 'POST':
        path = settings.MEDIA_ROOT+ '/documents/' +  _file.name
        response = FileResponse(open(path, 'rb'))
        return response


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def deleteFile(request, pk):
    _file = UserFiles.objects.get(id=pk)
    if request.method == 'POST':
        _file.delete()
        return redirect('user')

    context = {'item':_file}
    return render(request, 'gdrive/delete.html', context)
