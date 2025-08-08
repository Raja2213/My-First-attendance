from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, time, timedelta

class Attendance(models.Model):
    SHIFT_CHOICES = [
        ('A', 'Shift A'),
        ('B', 'Shift B'),
        ('C', 'Shift C'),
    ]

    LOCATION_CHOICES = [
        ('Chennai Office', 'Chennai Office'),
        ('Noida Office', 'Noida Office'),
        ('Bangalore Office', 'Bangalore Office'),
        ('Work from Home', 'Work from Home'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    project_name = models.CharField(max_length=100)
    shift = models.CharField(max_length=50, choices=SHIFT_CHOICES)
    # New field for location
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES, default='Work from Home') 
    time_in = models.TimeField(null=True, blank=True)
    time_out = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Attendance on {self.date}"

    def work_hours(self):
        if self.time_in and self.time_out:
            # We need to convert time objects to datetime objects for calculation
            # using a dummy date
            datetime_in = datetime.combine(self.date, self.time_in)
            datetime_out = datetime.combine(self.date, self.time_out)
            
            # If the user worked overnight, handle the date difference
            if datetime_out < datetime_in:
                # Add 24 hours (one day) to datetime_out if it's on the next day
                datetime_out = datetime_out + timedelta(days=1)
            
            duration = datetime_out - datetime_in
            hours, remainder = divmod(duration.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{int(hours)}h {int(minutes)}m"
        return "N/A"