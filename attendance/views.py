import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Attendance
from .forms import AttendanceForm, TimeOutForm, EditAttendanceForm
from django.http import HttpResponse

@login_required
def time_in(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            today = timezone.localdate()
            if Attendance.objects.filter(user=request.user, date=today, time_out__isnull=True).exists():
                messages.error(request, 'You are already timed in.')
            elif Attendance.objects.filter(user=request.user, date=today, time_out__isnull=False).exists():
                messages.error(request, 'You have already completed your attendance for today.')
            else:
                # The fix: Create the object explicitly to ensure all fields are populated correctly.
                Attendance.objects.create(
                    user=request.user,
                    project_name=form.cleaned_data['project_name'],
                    shift=form.cleaned_data['shift'],
                    date=today,
                    time_in=timezone.localtime(timezone.now()).time()
                )
                messages.success(request, 'You have successfully timed in!')
        else:
            messages.error(request, 'Invalid form submission.')
    return redirect('home')

@login_required
def time_out(request):
    if request.method == 'POST':
        today = timezone.localdate()
        
        try:
            # This will find the pending record that needs to be timed out
            attendance_record = get_object_or_404(
                Attendance, 
                user=request.user, 
                date=today, 
                time_out__isnull=True
            )
            
            # This is the crucial fix: explicitly update ONLY the time_out field
            attendance_record.time_out = timezone.localtime(timezone.now()).time()
            attendance_record.save(update_fields=['time_out'])
            
            messages.success(request, 'You have successfully timed out!')
            
        except Attendance.DoesNotExist:
            messages.error(request, 'You are not currently timed in.')
        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {e}')
            
    return redirect('home')

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('home')

    attendance_records = Attendance.objects.all().order_by('-date', '-time_in')
    
    date_filter = request.GET.get('date_filter')
    project_filter = request.GET.get('project_filter')

    if date_filter:
        attendance_records = attendance_records.filter(date=date_filter)
    
    if project_filter:
        attendance_records = attendance_records.filter(project_name=project_filter)

    projects = Attendance.objects.order_by('project_name').values_list('project_name', flat=True).distinct()

    context = {
        'attendance_records': attendance_records,
        'projects': projects,
        'date_filter': date_filter,
        'project_filter': project_filter,
    }
    return render(request, 'users/admin_dashboard.html', context)

@login_required
def edit_attendance(request, pk):
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to edit this record.')
        return redirect('home')

    record = get_object_or_404(Attendance, pk=pk)
    
    if request.method == 'POST':
        form = EditAttendanceForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, f"Record for {record.user.username} on {record.date} updated successfully.")
            return redirect('admin_dashboard')
    else:
        form = EditAttendanceForm(instance=record)
    
    context = {
        'form': form,
        'record': record
    }
    return render(request, 'users/edit_attendance.html', context)
    
@login_required
def delete_attendance(request, pk):
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to delete this record.')
        return redirect('admin_dashboard')
    
    record = get_object_or_404(Attendance, pk=pk)
    record.delete()
    messages.success(request, f"Attendance record for {record.user.username} on {record.date} has been deleted.")
    return redirect('admin_dashboard')

@login_required
def export_attendance(request):
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to export records.')
        return redirect('admin_dashboard')

    attendance_records = Attendance.objects.all().order_by('-date', '-time_in')
    
    date_filter = request.GET.get('date_filter')
    project_filter = request.GET.get('project_filter')
    
    # Fix for the ValidationError: Only filter if a valid value is provided
    if date_filter and date_filter != 'None':
        attendance_records = attendance_records.filter(date=date_filter)
    
    if project_filter and project_filter != 'None':
        attendance_records = attendance_records.filter(project_name=project_filter)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['User', 'Date', 'Project Name', 'Shift', 'Time In', 'Time Out'])

    for record in attendance_records:
        writer.writerow([
            record.user.username,
            record.date,
            record.project_name,
            record.shift,
            record.time_in,
            record.time_out,
        ])

    return response