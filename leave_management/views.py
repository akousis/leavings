# leave_management/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import LeaveApplicationForm
from .models import LeaveApplication, Employee # Σημαντικό: εισάγετε το Employee

# Renders the main landing page, now with leave history.
@login_required
def landing_page(request):
    """
    Ανακτά τις αιτήσεις άδειας του υπαλλήλου για εμφάνιση.
    """
    try:
        # Αναζητούμε το αντικείμενο Employee που αντιστοιχεί στον τρέχοντα χρήστη.
        employee = request.user.employee
        leave_applications = LeaveApplication.objects.filter(employee=employee)
    except Employee.DoesNotExist:
        leave_applications = [] # Επιστρέφουμε κενή λίστα αν δεν υπάρχει αντιστοίχιση
    
    context = {
        'leave_applications': leave_applications,
    }
    
    return render(request, 'leave_management/landing_page.html', context)

@login_required
def apply_for_leave(request):
    """
    Εμφανίζει τη φόρμα αίτησης άδειας και χειρίζεται την υποβολή της.
    """
    if request.method == 'POST':
        form = LeaveApplicationForm(request.POST)
        if form.is_valid():
            # Αποθηκεύουμε τη φόρμα χωρίς να κάνουμε ακόμα commit
            leave_application = form.save(commit=False)
            # Ορίζουμε τον υπάλληλο με βάση τον τρέχοντα συνδεδεμένο χρήστη
            leave_application.employee = request.user.employee
            # Τώρα αποθηκεύουμε την αίτηση στη βάση δεδομένων
            leave_application.save()
            return redirect('landing_page')
    else:
        # Για GET request, δημιουργούμε μια κενή φόρμα
        form = LeaveApplicationForm()
        
    return render(request, 'leave_management/apply_for_leave.html', {'form': form})

@login_required
def leave_history_view(request):
    """
    Renders the leave history for the logged-in employee.
    """
    return render(request, 'leave_management/leave_history.html')