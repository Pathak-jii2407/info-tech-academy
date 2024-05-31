from django.shortcuts import render, redirect
from .models import StudentStatus, TeacherAccount, StudentInfo, Edit
from datetime import date
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .sendmail import send
from django.contrib.auth.decorators import login_required



def index(request):
    today = date.today()
    present_students = StudentStatus.objects.filter(status_date=today, status='Present').values_list('name', flat=True)
    present = {'present_student': present_students}
    return render(request, 'base/NTI-Tech-Academy.html', present)


def teacher_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        teacher = TeacherAccount.objects.filter(username=username, password=password).first()
        
        if teacher is not None:
            return redirect('status')
        else:
            return render(request, 'base/teacher-signin.html', {'message': 'Not found as a teacher'})
            
    return render(request, 'base/teacher-signin.html')


def status(request):
    if request.method == 'POST':
        present_students = request.POST.getlist('attendance[]')
        today = date.today()
        
        for student_id in present_students:
            student = StudentInfo.objects.get(id=student_id)
            student_status, created = StudentStatus.objects.get_or_create(
                name=student.name,
                phone_num=student.phone_num,
                status_date=today,
                defaults={'status': 'Present'}
            )
            if not created:
                student_status.status = 'Present'
                student_status.save()
        
        return redirect('index')

    students = StudentInfo.objects.all()
    return render(request, 'base/NTI-Tech-status.html', {'students': students})

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
            myuser.first_name = firstname
            myuser.last_name = lastname
            

            student_data = StudentInfo(
                name=f'{firstname} {lastname}',
                phone_num=phone_num,
                email=email,
                username=username,
                password=password,
            )
            myuser.save()
            student_data.save()

            # send(user_email=email, first_name=firstname)
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
            return student_account(request,username,password)
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'base/signin.html')

def signout(request):
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('index')

def student_account(request, username=None, password=None):
    try:
        if request.method == 'POST' and username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                student = StudentInfo.objects.filter(username=username, password=password).first()
                if student:
                    data = Edit.objects.filter(student_info=student).first()
                    return render(request, 'base/NTI-Tech-Academy-student-Account.html', {'student': student, 'data': data})
        
        return redirect('signin')
    except:
        return redirect('signin')




@login_required
def edit(request):
    if request.method == 'POST':
        if 'image' in request.FILES and 'subject' in request.POST:
            image = request.FILES['image']
            subject = request.POST['subject']
            username = request.user.username  # Accessing the username of the currently authenticated user
            studentinfo = StudentInfo.objects.get(username=username)
            Edit.objects.create(student_info=studentinfo, image=image, subject=subject)
            return redirect('index')
    return redirect('signin')



def teacher_account(request):
    teachers = TeacherAccount.objects.all()
    return render(request, 'base/NTI-Tech-Academy-teacher-Account.html', {'teachers': teachers})


def search_account(request):
    query = request.GET.get('query', '').strip()
    
    students = []
    teachers = []
    
    if query:
        students = StudentInfo.objects.filter(name__icontains=query)
        teachers = TeacherAccount.objects.filter(name__icontains=query)
        
    return render(request, 'base/search_account.html', {'students': students, 'teachers': teachers, 'query': query})
