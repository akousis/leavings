"""
This module registers the models with the Django admin site.
It also includes custom configurations to improve the usability and
display of these models in the admin interface.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Organization, Employee, LeaveType, LeaveApplication

# Register the User model with the admin site.
# For simplicity, we are making the User model read-only in the admin,
# as we assume user creation will happen via a custom authentication service.
@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """
    Custom admin class for the User model.
    It extends Django's default UserAdmin but makes the fields read-only
    to prevent manual changes in the admin panel.
    """
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('username', 'first_name', 'last_name', 'email', 'last_login', 'date_joined', 'is_superuser', 'is_staff', 'groups', 'user_permissions')
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """
    Admin class for the Organization model.
    Customizes the list display to show key organization details.
    """
    list_display = ('name', 'director_name', 'contact_email', 'contact_phone')
    search_fields = ('name', 'director_name')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """
    Admin class for the Employee model.
    Customizes the display and search functionality for employee profiles.
    """
    # Use 'user__first_name' and 'user__last_name' to traverse the ForeignKey relationship
    list_display = ('user_full_name', 'am', 'afm', 'organization', 'specialty', 'is_hr', 'is_director')
    search_fields = ('user__first_name', 'user__last_name', 'am', 'afm', 'specialty')
    list_filter = ('organization', 'specialty', 'is_hr', 'is_director')
    
    # Custom method to display the full name of the user
    def user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    user_full_name.short_description = "Ονοματεπώνυμο" # Sets the column header name

@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    """
    Admin class for the LeaveType model.
    Customizes the list display for leave types.
    """
    list_display = ('name', 'max_days', 'max_months', 'is_long_term')
    search_fields = ('name',)
    list_filter = ('is_long_term',)


@admin.register(LeaveApplication)
class LeaveApplicationAdmin(admin.ModelAdmin):
    """
    Provides a rich view with filters and search functionality for leave requests.
    """
    list_display = ('employee_full_name', 'leave_type', 'start_date', 'end_date', 'status', 'protocol_number')
    search_fields = ('employee__user__first_name', 'employee__user__last_name', 'employee__am', 'protocol_number')
    list_filter = ('status', 'leave_type', 'start_date', 'end_date')
    readonly_fields = ('leave_days_count', 'leave_months_count', 'protocol_number')
    
    # Custom method to display the full name of the employee
    def employee_full_name(self, obj):
        return f"{obj.employee.user.first_name} {obj.employee.user.last_name}"
    employee_full_name.short_description = "Υπάλληλος"
