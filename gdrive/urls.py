from django.urls import path
import  django.contrib.auth.views as auth_views
from . import views

urlpatterns = [
        path('register/', views.register, name = 'register'),
        path('login/', views.loginPage, name = 'login'),
        path('logout/', views.logoutUser, name = 'logout'), 
        path('', views.home, name = 'home'),
        path('upload_file/', views.uploadFile, name = 'upload_file'),
        path('user/', views.userPage, name = 'user'),
        path('file_error', views.fileError, name = 'file_error'),
        path('download_file/<str:pk>', views.downloadFile, name = 'download_file'),
        path('account/', views.accountSettings, name = 'account'),
        path('delete_file/<str:pk>', views.deleteFile, name = 'delete_file'),
           path('reset_password/',
        auth_views.PasswordResetView.as_view(template_name="gdrive/password_reset.html"),
        name="reset_password"),

    path('reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(template_name="gdrive/password_reset_sent.html"),
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name="gdrive/password_reset_form.html"),
        name="password_reset_confirm"),

    path('reset_password_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name="gdrive/password_reset_done.html"),
        name="password_reset_complete"), 
        
        ]

