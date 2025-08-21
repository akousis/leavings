from django import forms
from .models import LeaveApplication, LeaveType

class LeaveApplicationForm(forms.ModelForm):
    """
    Form for submitting a leave application.
    """
    class Meta:
        model = LeaveApplication
        fields = ['leave_type', 'start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Συμπληρώστε τον λόγο της άδειας'}),
        }

