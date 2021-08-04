from student_management_app.models import SessionYearModel, Subjects
from django.shortcuts import render


def staff_home(request):
    return render(request, 'staff_template/staff_home.html')

def staff_take_attendance(request):
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    session_years=SessionYearModel.object.all()
    return render(request, 'staff_template/staff_take_attendance.html', {"subjects": subjects, "session_years": session_years})