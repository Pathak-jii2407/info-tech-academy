from django.shortcuts import render, redirect
from .models import StudentStatus, TeacherAccount, StudentInfo, Edit
from datetime import date
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .sendmail import send
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required



def index(request):
    today = date.today()
    present_students = StudentStatus.objects.filter(status_date=today, status='Present').values_list('name', flat=True)
    teachers = TeacherAccount.objects.all()
    if User is not None:
        context = {
            'present_student': present_students,
            'teachers': teachers,
            'user': request.user,
        }
    try:
        try:
            teacher_data = TeacherAccount.objects.get(username=request.user)
            context['data']=teacher_data
        except:
            student_data = StudentInfo.objects.get(username=request.user)
            context['data']=student_data
    except:
        pass

    return render(request, 'base/NTI-Tech-Academy.html', context)

def teacher_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            teacher = TeacherAccount.objects.get(username=username)
        except TeacherAccount.DoesNotExist:
            teacher = None
        
        if teacher:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=password)
                user.is_active = True
                user.is_staff = True
                user.is_superuser = True
                user.save()
            else:
                user = authenticate(username=username, password=password)
            if user:
                login(request, user) 
                return redirect('index')
            else:
                return render(request, 'base/teacher-signin.html', {'message': 'Not found as a teacher or incorrect password'})
    return render(request, 'base/teacher-signin.html')




@staff_member_required
def status(request):
    if request.method == 'POST':
        present_students = request.POST.getlist('attendance[]')
        today = date.today()

        all_students = StudentInfo.objects.all()

        for student in all_students:
            status = 'Present' if str(student.id) in present_students else 'Absent'
            student_status, created = StudentStatus.objects.get_or_create(
                name=student.name,
                phone_num=student.phone_num,
                status_date=today,
                defaults={'status': status}
            )
            if not created:
                student_status.status = status
                student_status.save()

        return redirect('index')

    students = StudentInfo.objects.all()
    return render(request, 'base/NTI-Tech-status.html', {'students': students, 'user': request.user})


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('fname')
        lastname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_num = request.POST.get('phone_num')
        
        try:
            if User.objects.filter(username=username).exists() :
                messages.error(request, "User with this username already exists")
                return redirect('signup')
            
            if User.objects.filter(email=email).exists() :
                messages.error(request, "User with this email already exists")
                return redirect('signup')
            if StudentInfo.objects.filter(phone_num=phone_num).exists():
                messages.error(request, "User with this phone number already exists")
                return redirect('signup')
            
            
            myuser = User.objects.create_user(username, email, password)
            myuser.first_name = firstname.capitalize()
            myuser.last_name = lastname.capitalize()
            
            student_data = StudentInfo(
                name=f'{firstname} {lastname}',
                phone_num=phone_num,
                email=email,
                username=username,
                password=password,
            )
            myuser.save()
            student_data.save()

            send(user_email=email, first_name=firstname)
            user = authenticate(username=username, password=password)
            return redirect('signin')
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect('signup')
    
    return render(request, 'base/signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return student_account(request)
        
        
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'base/signin.html')

def student_account(request):
    try:
        student = StudentInfo.objects.get(username=request.user.username)
        data = Edit.objects.filter(student_info=student).last()
        return render(request, 'base/NTI-Tech-Academy-student-Account.html', {'student': student, 'data': data})

    except StudentInfo.DoesNotExist:
        pass

    return redirect('signin')

def signout(request):
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('index')

@login_required
def edit(request):
    if request.method == 'POST':
        if 'image' in request.FILES and 'subject' in request.POST:
            image = request.FILES['image']
            subject = request.POST['subject']
            student = StudentInfo.objects.get(username=request.user.username)
            data = Edit.objects.create(student_info=student, image=image, subject=subject)
            return render(request, 'base/NTI-Tech-Academy-student-Account.html', {'student': student, 'data': data})
    return redirect('signin')

def teacher_account(request):
    teachers = TeacherAccount.objects.all()
    return render(request, 'base/NTI-Tech-Academy-teacher-Account.html', {'teachers': teachers})


def dashboard(request):
    present_data = StudentStatus.objects.all()
    return render(request, 'base/dashboard.html', {'present': present_data})
