"""
This module defines the models for the leave management system.
It includes custom user models, organization details, employee profiles, leave types, and leave applications.
These models are used to manage the data related to leave requests and employee information in the system.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from workalendar.europe import Greece
from datetime import date
from decimal import Decimal



# Need to configure settings.py to point to this custom User model.
# AUTH_USER_MODEL = 'leave_management.User'
class User(AbstractUser):
    """
    A custom User model that extends Django's AbstractUser.
    This provides more flexibility than the default User model.
    It already includes all the essential fields like username, password, first_name, last_name, and email.
    Will change for sch authentication service.
    """
    pass  # A placeholder. User class is being defined but there are no additional fields for now.

class Organization(models.Model):
    """
    Represents a school, department, or central directorate.
    An employee will be linked to a single organization.
    """
    name = models.CharField(max_length=255, unique=True, verbose_name="Οργανισμός")
    address = models.TextField(blank=True, verbose_name="Διεύθυνση")
    director_name = models.CharField(max_length=255, blank=True, verbose_name="Όνομα Διευθυντή")
    contact_email = models.EmailField(blank=True, verbose_name="Email Επικοινωνίας")
    contact_phone = models.CharField(max_length=20, blank=True, verbose_name="Τηλέφωνο Επικοινωνίας")

    def __str__(self):
        """
        Returns the name of the organization for easy identification.
         It is a special method in Python, often referred to as a "dunder" method. It defines the "official" string representation of an object.
        """
        return self.name

class Employee(models.Model):
    """
    Stores a profile for each employee, linked to a custom User and an Organization.
    This model serves as the base for all employee types.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Χρήστης")
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Οργανισμός")
    fathers_name = models.CharField(max_length=255, verbose_name="Όνομα Πατέρα")
    am = models.CharField(max_length=20, unique=True, verbose_name="Αριθμός Μητρώου")
    afm = models.CharField(max_length=20, unique=True, verbose_name="Αριθμός Φορολογικού Μητρώου")    
    hire_date = models.DateField(verbose_name="Ημερομηνία Πρόσληψης")
    specialty = models.CharField(max_length=255, verbose_name="Ειδικότητα")
    telephone = models.CharField(max_length=20, blank=True, verbose_name="Τηλέφωνο")
    mobile = models.CharField(max_length=20, blank=True, verbose_name="Κινητό")
    is_hr = models.BooleanField(default=False, verbose_name="Υπάλληλος HR")
    is_director = models.BooleanField(default=False, verbose_name="Διευθυντής")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class LeaveType(models.Model):
    """
    Defines the different types of leave that an employee can request.
    """
    name = models.CharField(max_length=255, unique=True, verbose_name="Τύπος Άδειας")
    max_days = models.IntegerField(verbose_name="Μέγιστες Ημέρες Άδειας")
    max_months = models.IntegerField(verbose_name="Μέγιστοι Μήνες Άδειας", default=0, help_text="Συμπληρώστε μόνο για μακροπρόθεσμες άδειες (μήνες).")
    is_long_term = models.BooleanField(default=False, verbose_name="Μακροχρόνια Άδεια")

    def __str__(self):
        return self.name

class LeaveApplication(models.Model):
    """
    Stores a single leave request, its state, and its details.
    The 'status' field directly implements the logic from our state machine diagram.
    """
    # Choices for the 'status' field
    STATUS_CHOICES = (
        ('Submitted', 'Submitted'),
        ('Received', 'HR Received'),
        ('Awaiting_Documentation', 'Awaiting Employee Documentation'),
        ('Ready_for_Approval', 'Ready for Director Approval'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Canceled', 'Canceled'),
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Υπάλληλος")
    leave_type = models.ForeignKey(LeaveType, on_delete=models.PROTECT, verbose_name="Τύπος Άδειας")
    start_date = models.DateField(verbose_name="Ημερομηνία Έναρξης")
    end_date = models.DateField(verbose_name="Ημερομηνία Λήξης")
    leave_days_count = models.IntegerField(verbose_name="Αριθμός Ημερών Άδειας")
    leave_months_count = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'), verbose_name="Αριθμός Μηνών Άδειας")
    reason = models.TextField(verbose_name="Αιτιολογία")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Submitted', verbose_name="Κατάσταση")
    rejection_reason = models.TextField(blank=True, null=True, verbose_name="Λόγος Απόρριψης")
    protocol_number = models.CharField(max_length=255, blank=True, null=True, unique=True, verbose_name="Αριθμός Πρωτοκόλλου")

    def __str__(self):
        return f"Leave application for {self.employee.user.username} ({self.status})"
    
    def calculate_working_days(self):
        """
        Calculates working days, including holidays for Greece.
        """
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValueError("Start date cannot be after end date.")
            # Use Greece calendar to calculate working days
            cal = Greece()
            return cal.get_working_days_delta(self.start_date, self.end_date)
        return 0
    
    def calculate_months(self):
        """
        Calculates the number of months between two dates as a floating-point number.
        """
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValueError("Start date cannot be after end date.")
            
            # Calculate total days and divide by the average number of days in a month.
            total_days = (self.end_date - self.start_date).days
            return Decimal(total_days) / Decimal(30.44)
        return Decimal(0.00)

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to automatically calculate the leave days or months count
        based on the leave type before saving the object.
        """
        if self.leave_type and self.leave_type.is_long_term:
            # It's a long-term leave, calculate months and set days to 0
            self.leave_months_count = self.calculate_months()
            self.leave_days_count = 0
        else:
            # It's a short-term leave, calculate days and set months to 0
            self.leave_days_count = self.calculate_working_days()
            self.leave_months_count = 0
            
        super().save(*args, **kwargs)