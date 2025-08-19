from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import LeaveApplicationForm

# Renders the main landing page
def landing_page(request):
    return render(request, 'leave_management/landing_page.html')

@login_required # Ensure user is logged in to access this view
def apply_for_leave(request):
    """
    Renders the leave application form and handles form submission.
    """
    if request.method == 'POST':
        form = LeaveApplicationForm(request.POST)
        if form.is_valid():
            # Save the form data but do not commit to the database yet
            leave_application = form.save(commit=False)
            # Set the employee field to the current user
            leave_application.employee = request.user
            # Save the instance to the database
            leave_application.save()
            # Redirect to the landing page after successful submission
            return redirect('landing_page')
    else:
        # If the request is GET, instantiate an empty form
        form = LeaveApplicationForm()

    return render(request, 'leave_management/apply_for_leave.html', {'form': form})
