from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from student_management_app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

def showDemoPage(request):
    return render(request,"demo.html")

def ShowloginPage(request):
        return render(request,"login_page.html")

def doLogin(request):
    if request.method !="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user=EmailBackEnd.authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
        if user !=None:  
            login(request,user)
            if user.user_type =="1":
              return HttpResponseRedirect("/admin_home") 
            #return HttpResponse("Email: "+request.POST.get("email")+"Password: "+request.POST.get("password"))  
            elif user.user_type =="2":
                return HttpResponse("Staff Login"+str(user.user_type))
            else:
                return HttpResponse("Student Login"+str(user.user_type))    
        else:
            messages.error(request,'Invalid Login Details')
            return HttpResponseRedirect("/") 

def GetUserDetails(request):
    if request.user !=None:
        return HttpResponse("User : " + request.user.email + "usertype: " + request.user.user_type)
    else:
        return HttpResponse("Please Login First" ) 

def logout_user(request):
    logout(request)
    return HttpResponse("/")            


        