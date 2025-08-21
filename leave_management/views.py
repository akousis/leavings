from django.shortcuts import render, redirect
from django.http import HttpResponse

# You'll need to import your LeaveApplication model here once it's created.
# from .models import LeaveApplication

# This view renders the main landing page of the application.
def landing_page(request):
    """
    Renders the landing page of the leave management application.
    """
    return render(request, 'landing_page.html')

# This view renders the form for a new leave application.
def apply_for_leave(request):
    """
    Renders the form page for a new leave application.
    """
    return render(request, 'apply_for_leave.html')

# This view will handle the submission of the leave application form.
def add_leave_application(request):
    """
    Handles the submission of a new leave application.
    """
    if request.method == 'POST':
        # You will process the form data here once the model is defined.
        # For now, we'll just redirect to the history page.
        # Example of processing data:
        # employee_name = request.POST.get('employee_name')
        # start_date = request.POST.get('start_date')
        # end_date = request.POST.get('end_date')
        # LeaveApplication.objects.create(employee=employee_name, ...)
        
        # After processing, redirect to the leave history view.
        return redirect('leave_history_view')
    
    # If the request method is not POST, redirect to the apply form.
    return redirect('apply_for_leave')

# This view displays a list of all submitted leave applications.
def leave_history_view(request):
    """
    Renders the page showing the history of all leave applications.
    """
    # This is a placeholder list. Once you have a model, you will fetch data from it.
    # For now, we'll use a sample list to test the template.
    sample_leave_applications = [
        {'employee': 'Jane Doe', 'leave_type': 'Vacation', 'start_date': '2025-07-20', 'end_date': '2025-07-25', 'status': 'Pending'},
        {'employee': 'John Smith', 'leave_type': 'Sick Leave', 'start_date': '2025-07-15', 'end_date': '2025-07-16', 'status': 'Approved'},
    ]

    context = {
        'leave_applications': sample_leave_applications
    }
    
    return render(request, 'leave_history.html', context)
