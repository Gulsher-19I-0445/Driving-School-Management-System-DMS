from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login as authLogin, logout, authenticate
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from .models import customer, attendance
from .models import Teacher
from django import forms
# Create your views here.
from .forms import MyForm
from .backend import AuthBackend, Teacher_AuthBackend
from django import forms
from django import forms
# Create your views here.


def my_form(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['name']
            tempform = AuthBackend.authenticate(request, username=username, password=123)
            if tempform is None:

            #form.clean_name()
                form.save()
                messages.error(request, 'User successfully registered')
            else:
                messages.error(request, 'username already registered')
                #return redirect('register')
    else:
        form = MyForm()
        #messages.error(request, 'username or password not correct')
    return render(request, 'accounts/register.html', {'form': form})

def home(request):
    entries = customer.objects.all()
    context = {"entries": entries}
    return render(request,'accounts/home.html',{})

def register(request):
    context = {}
    context['form'] = InputForm()
    return render(request, "accounts/register.html", context)

@csrf_exempt
def login(request,backend='accounts.backend.AuthBackend'):
    #print("hjhjh--->",request.user.name)
    #if request.user is not None:
     #   print(request.user)
      #  return redirect('MainPage')
    next_url = request.GET.get('next')
    print(request.user)
    if request.method=='POST':



        username=request.POST.get('username')
        password=request.POST.get('password')
        if 'student' in request.POST:
            #form=authenticate(request,username=username,password=password)
            form= AuthBackend.authenticate(request, username=username, password=password)
            #print("form---->",form.email)
            if form is not None:
                # print('hellllllllllllldsjdbjad\n')
                # if form.is_active:

                print(request.user)
                authLogin(request, form,backend='accounts.backend.AuthBackend')

                user_id=request.user.id
                print(request.user)
                entries = customer.objects.all()
                # print(f"Username --> {request.user.customer_uuid}")
                context = {'foo': 'bar'}
                #if request.user.is_authenticated():
                 #   print("authern")
                #return redirect('MainPage')
                #return HttpResponseRedirect(reverse('MainPage'))
                return render(request, 'accounts/MainPage.html', {"user_id":request.user.id})
            # else:
            # print(forms.ValidationError);
            else:
                messages.error(request, 'username or password not correct')
                return redirect('login')


     #return render(request, 'accounts/login.html')

        elif 'instructor' in request.POST:
            form = Teacher_AuthBackend.authenticate(request, username=username, password=password)
            if form:
                # print('hellllllllllllldsjdbjad\n')
                # if form.is_active:
                authLogin(request, form,backend='accounts.backend.Teacher_AuthBackend')
                entries = Teacher.objects.all()
                # print(f"Username --> {request.user.customer_uuid}")
                context = {'foo': 'bar'}
                dashboard(request)
                return render(request, 'accounts/MainPage.html', {"user_id": request.user.id})
                #return render(request, 'accounts/MainPage.html', {})
            else:
                messages.error(request, 'username or password not correct')
                return redirect('login')


    else:
        #print("Mera naaem--->",request.user.name)
        if next_url:
            return redirect(next_url)
        print("Hello")
        form = AuthenticationForm()
        #print(form)
    #print("hello")


        return render(request, 'accounts/login.html', {form: 'form'})


def myauthenticate( username=None, password=None):

    try:

        user = customer.objects.get(name=username)

            #  Check the password is the reverse of the username
        if check_password(password, user.password_en):
                # Yes? return the Django user object
            #user.save()
            return user
        else:
                # No? return None - triggers default login failed
            return None
    except customer.DoesNotExist:
            # No user was found, return None - triggers default login failed
        return None

    # Required for your backend to work properly - unchanged in most scenarios
'''def get_user(self, user_id):
    try:
        return customer.objects.get(pk=user_id)
    except customer.DoesNotExist:
        return None'''

def myauthenticateteacher(username=None, password=None):
    try:

        teacher = Teacher.objects.get(name=username)

        if check_password(password, teacher.password_en):
            return teacher
        else:
            return None
    except Teacher.DoesNotExist:
        return None

def check_password(password1,password2):
    if password2==password1:
        return True
    else:
        return False

def getCurrentUserName(request):
    return {request.user.name}

#@login_required
def planSelection(request):

    if request.method=='POST':
        temp=request.user
        if 'plan1' in request.POST:
            temp.plan='PLan1'
        elif 'plan2' in request.POST:
            temp.plan='Plan2'
        elif 'plan3' in request.POST:
            temp.plan='Plan3'
        TData=Teacher.objects.all()
        if TData:
            for field in TData:
                if field.studentName is None:
                    #tempTeacher=Teacher.objects.get(field.name)
                    temp.myteacher = field
                    field.studentName = temp
                    field.save()
                    break


        temp.isRegistered=True
        temp.save()
        return redirect('MainPage')
    #myuser=request.POST.get("user","")
    #print(getCurrentUserName(request))
    #print(request.POST.get(name))
    return render(request, 'accounts/planSelection.html',{'userprofile':request.user})
    #else:
     #   return render(request, 'accounts/MainPage.html', {})

def TeacherInfo(request):
    if request.method == 'POST':
        return redirect('MainPage')
    return render(request, 'accounts/myTeacherInfo.html', {'userprofile': request.user})

def UserPlan(request):
    if request.method == 'POST':
        return redirect('MainPage')
    return render(request, 'accounts/UserPlan.html', {'userprofile': request.user})

def MarkAttendance(request):
    if request.method == 'POST':
        date1=request.POST.get("AttendanceDate")
        p_status=request.POST.get("Present/Absent")

        attend=attendance(studentName=request.user.studentName,date=date1,status=p_status)
        attend.save()


        return redirect('MarkAttendance')
    return render(request, 'accounts/MarkAttendance.html', {'userprofile': request.user})

def dashboard(request):
    #return redirect('login')
    username = request.POST.get('name')
    print("g--->",username)
    #print("Inplan---->", request.user.name)
    return render(request, 'accounts/MainPage.html',{})

def Attendance(request):
    if request.method == 'POST':
        return redirect('MainPage')
    attendance_list = attendance.objects.all()
    tempDate=[]
    tempStatus=[]

    for x in attendance_list:
        if x.studentName==request.user:
            tempDate.append(x.date)
            tempStatus.append(x.status)
    finalList=zip(tempDate,tempStatus)
    finalList=list(finalList)
    context_dict = {'attendance': finalList}
    return render(request, 'accounts/attendance.html', context_dict)