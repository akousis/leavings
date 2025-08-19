from django import forms
from .models import LeaveApplication

class LeaveApplicationForm(forms.ModelForm):
    """
    Form for submitting a leave application.
    """
    class Meta:
        model = LeaveApplication
        fields = ['start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter the reason for your leave here...'}),
        }
