import json
from django.http.response import HttpResponse, JsonResponse
from student_management_app.models import Attendance, AttendanceReport, SessionYearModel, Students, Subjects
from django.shortcuts import render
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt


def staff_home(request):
    return render(request, 'staff_template/staff_home.html')

def staff_take_attendance(request):
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    session_years=SessionYearModel.objects.all()
    return render(request, 'staff_template/staff_take_attendance.html', {"subjects": subjects, "session_years": session_years})

@csrf_exempt
def get_students(request):
    subject_id=request.POST.get('subject')
    session_year=request.POST.get('session_year')
    subject=Subjects.objects.get(id=subject_id)
    session_model=SessionYearModel.object.geet(id=session_year)
    students=Students.objects.filter(course_id=subject.course_id, session_year_id=session_model)
    #student_data=serializers.serialize("python",students)
    list_data=[]
    for student in students:
        data_small={"id":student.admin.id, "name":student.admin.first_name+" "+student.admin.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

    #return HttpResponse(students) 

@csrf_exempt
def save_attendance_data(request):
    student_ids=request.POST.get("student_ids[]")
    subject_id=request.POST.get("subject_id")
    attendance_date=request.POST.get("attendance_date")
    session_year_id=request.POST.get("session_year_id")
    
    subject_model=Subjects.objects.get(id=subject_id)
    session_model=SessionYearModel.object.get(id=session_year_id)
    json_student=json.loads(student_ids)
    #print(data[0]['id'])
    try:
        attendance=Attendance(subject_id=subject_model, attendance_date=attendance_date, session_year_id=session_model)   
        attendance.save()

        for stud in json_student:
            student=Students.objects.get(admin_id=stud['id'])
            attendance_report=AttendanceReport(student_id=student, attendance_id=attendance, status=stud['status'])
            attendance_report.save()        
        return HttpResponse("Ok")
    except:
        return HttpResponse("ERR")

def staff_update_attendance(request):
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    session_year_id=SessionYearModel.objects.all()
    return render(request,"staff_template/staff_update_attendance.html",{"subjects":subjects, "session_year_id":session_year_id})

@csrf_exempt
def get_attendance_dates(request):
    subject=request.POST('subject')
    session_year_id=request.POST('session_year_id')
    subject_obj=Subjects.objects.get(id=subject)
    session_year_obj=SessionYearModel.object.get(id=session_year_id)
    attendance=Attendance.objects.filter(subject_id=subject_obj, session_year_id=session_year_obj)
    
    attendance_obj=[]
    for attendance_single in attendance:
        data={"id":attendance_single.id, "attendance_date":str(attendance_single.attendance_date), "session_year_id":attendance_single.session_year_id.id}
        attendance_obj.append(data)
    return JsonResponse(json.dumps(attendance_obj), safe=False)    


