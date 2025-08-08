from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from attendance import views as attendance_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.home, name='home'),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('time_in/', attendance_views.time_in, name='time_in'),
    path('time_out/', attendance_views.time_out, name='time_out'),
    path('admin_dashboard/', attendance_views.admin_dashboard, name='admin_dashboard'),
    path('edit_attendance/<int:pk>/', attendance_views.edit_attendance, name='edit_attendance'),
    path('delete_attendance/<int:pk>/', attendance_views.delete_attendance, name='delete_attendance'), # Corrected
    path('export_attendance/', attendance_views.export_attendance, name='export_attendance'), # Added
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]