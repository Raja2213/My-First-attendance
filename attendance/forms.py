from django import forms
from .models import Attendance

class AttendanceForm(forms.ModelForm):
    # This is a sample list of projects. Replace with your actual projects.
    PROJECT_CHOICES = [
        ('Project Alpha', 'Project Alpha'),
        ('Project Beta', 'Project Beta'),
        ('Project Gamma', 'Project Gamma'),
    ]

    project_name = forms.CharField(
        label='Project Name',
        widget=forms.Select(choices=PROJECT_CHOICES, attrs={'class': 'form-control'})
    )

    class Meta:
        model = Attendance
        # Add the 'location' field to the list of fields
        fields = ['project_name', 'shift', 'location']
        widgets = {
            'shift': forms.Select(choices=Attendance.SHIFT_CHOICES, attrs={'class': 'form-control'}),
            # Add the widget for the new location field
            'location': forms.Select(choices=Attendance.LOCATION_CHOICES, attrs={'class': 'form-control'}),
        }

class TimeOutForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = [] # No fields needed for the time out action

# NEW FORM FOR EDITING
class EditAttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        # Add the 'location' field to the list of fields
        fields = ['date', 'project_name', 'shift', 'location', 'time_in', 'time_out']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time_in': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'time_out': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'project_name': forms.TextInput(attrs={'class': 'form-control'}),
            'shift': forms.TextInput(attrs={'class': 'form-control'}),
            # Add the widget for the new location field
            'location': forms.Select(choices=Attendance.LOCATION_CHOICES, attrs={'class': 'form-control'}),
        }