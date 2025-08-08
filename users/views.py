from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from .forms import UserRegisterForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from attendance.models import Attendance # ADDED IMPORT
from attendance.forms import AttendanceForm, TimeOutForm, EditAttendanceForm
from django.http import HttpResponse

# The home view should stay here, as it's a user-specific page.
@login_required
def home(request):
    today = timezone.localdate()
    
    # Check if a time-out is pending
    pending_record = Attendance.objects.filter(user=request.user, date=today, time_out__isnull=True).first()
    
    # Check if attendance is already completed for the day
    completed_record = Attendance.objects.filter(user=request.user, date=today, time_out__isnull=False).first()

    # Get all attendance history for the user, ordered by date
    user_attendance_history = Attendance.objects.filter(user=request.user).order_by('-date', '-time_in')
    
    if pending_record:
        # A record exists but is not timed out. Display the time out form.
        context = {
            'has_timed_in': True,
            'user_attendance_history': user_attendance_history,
            'pending_record': pending_record,
        }
    elif completed_record:
        # Attendance is completed for the day. Display a message.
        context = {
            'has_timed_in': False,
            'attendance_completed': True,
            'user_attendance_history': user_attendance_history,
        }
    else:
        # No attendance record for today. Display the time in form.
        form_in = AttendanceForm()
        context = {
            'has_timed_in': False,
            'attendance_completed': False,
            'form_in': form_in,
            'user_attendance_history': user_attendance_history,
        }

    return render(request, 'users/home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'users/profile.html')

def custom_logout_view(request):
    if request.method == 'POST':
        auth_logout(request)
        messages.success(request, "Logged out successfully!")
        return redirect('login')
    return redirect('home')

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('password_change_done')

    def form_valid(self, form):
        response = super().form_valid(form)
        # This part of the code assumes you have a profile model related to the user
        # self.request.user.profile.must_change_password = False
        # self.request.user.profile.save()
        messages.success(self.request, "Your password has been changed successfully.")
        return response

@login_required
def dashboard(request):
    context = {
        'username': request.user.username,
    }
    return render(request, 'users/dashboard.html', context)

@login_required
def all_users(request):
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('dashboard')
    
    all_users = User.objects.all().order_by('username')
    return render(request, 'users/all_users.html', {'all_users': all_users})