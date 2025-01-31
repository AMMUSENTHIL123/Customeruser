from django.shortcuts import render,redirect

# Create your views here.

from django.db import models
from .models import Teacher
from .models import Student
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
import random
from django.contrib.auth import logout
     


def home(request):
    return render (request, 'home.html')



def ahome(request):
     # Count of unapproved users (status = 0)
    unapproved_count = CustomUser.objects.filter(status=0).count()
    count = unapproved_count - 1  # This line might be a mistake, as it subtracts 1 from the count

    print(count)  # This line is for debugging and can be removed later
    return render (request, 'adminhome.html', {'unapproved_count': count})


def shome(request):
    return render (request, 'studenthome.html')

def thome(request):
    return render (request, 'teacherhome.html')

def login1(request):
    
    return render(request, 'login.html')  

def student1(request):
        
    
        return render(request, 'studentsignup.html') 
def teacher1(request):
     
     return render(request, 'teachersignup.html')



def studentsignup(request):
  if request.method == 'POST':
    name= request.POST.get('name')
    course = request.POST.get('course')
    age = request.POST.get('age')
    email = request.POST.get('email')
    username = request.POST.get('username')
    phone_number = request.POST.get('phone_number')
    image = request.FILES.get('image')
    user_type = request.POST['text']


    # Check if username already exists
    if CustomUser.objects.filter(username=username).exists():
            messages.success(request, 'Username already exists. Please choose another.')
            return redirect('student1')

    
    if CustomUser.objects.filter(email=email).exists():
            messages.success(request, 'Email already exists. Please choose another.')
            return render(request, 'studentsignup.html') 
    #Add data to the database (replace with your model)
     # Create user and teacher entries after all validations pass
    user = CustomUser.objects.create_user(
            username=username,
            first_name=name,
            email=email,
            user_type=user_type
        )

    student = Student(
            user=user,  # Associate the teacher with the created user
            course=course,  # Assuming 'sell' is the selected course
            Age=age,
            Phone_number=phone_number,
            Image=image
        )
    student.save()

    messages.success(request, 'Registration Successful! Please wait for admin approval.')
    return redirect('student1')  # Redirect to the home page after successful creation

  return render(request, 'studentsignup.html')


def teachersignup(request):
  if request.method == 'POST':
    name= request.POST.get('name')
    course = request.POST.get('course')
    age = request.POST.get('age')
    email = request.POST.get('email')
    username = request.POST.get('username')
    phone_number = request.POST.get('phone_number')
    image = request.FILES.get('image')
    user_type = request.POST['text']


    # Check if username already exists
    if CustomUser.objects.filter(username=username).exists():
            messages.success(request, 'Username already exists. Please choose another.')
            return redirect('teacher1')

    
    if CustomUser.objects.filter(email=email).exists():
            messages.success(request, 'Email already exists. Please choose another.')
            return render(request, 'teachersignup.html') 
    #Add data to the database (replace with your model)
     # Create user and teacher entries after all validations pass
    user = CustomUser.objects.create_user(
            username=username,
            first_name=name,
            email=email,
            user_type=user_type
        )

    teacher = Teacher(
            user=user,  # Associate the teacher with the created user
            course=course,  # Assuming 'sell' is the selected course
            Age=age,
            Phone_number=phone_number,
            Image=image
        )
    teacher.save()

    messages.success(request, 'Registration Successful! Please wait for admin approval.')
    return redirect('teacher1')  # Redirect to the home page after successful creation

  return render(request, 'teachersignup.html')



def loginhome(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.user_type == '1':
                login(request, user)
                return redirect('ahome')
            elif user.user_type == '2':
                login(request, user)
                return redirect('thome')
            elif user.user_type == '3':
                login(request, user)
                return redirect('shome')

        else:
            messages.info(request, "Invalid username or password")
            return redirect('login1')


def ad(request):
    users = CustomUser.objects.filter(~Q(user_type="1"))  # Filter out users with user_type = 1

    # teachers = Teacher.objects.filter(user__in=users) 
    # students = Student.objects.filter(user__in=users) 

    unapproved_count = CustomUser.objects.filter(status=0).count()
    count = unapproved_count - 1  # This line might be a mistake, as it subtracts 1 from the count

    print(count)  # This line is for debugging and can be removed later

    return render(request, 'showadtable.html', {'user_data': users, 'unapproved_count':count})



def approve(request, k):
    usr = CustomUser.objects.get(id=k)
    usr.status = 1
    usr.save()

    if usr.user_type == '2': 
        tea = Teacher.objects.get(user=k) 
        password = str(random.randint(100000, 999999)) 
        print(password)
        usr.set_password(password)  # Use set_password for secure password hashing
        usr.save() 

        # Send email notification with the generated password
        send_mail(
            'Teacher Account Approval',
            f'Your account has been approved. Your temporary password is: {password}',
            settings.EMAIL_HOST_USER,  # Replace with your email settings
            [tea.user.email],  # Send email to the teacher's email
            
        )

    elif usr.user_type == '3': 
        # Handle student approval logic here (if applicable)
        stud = Student.objects.get(user=k) 
        password = str(random.randint(100000, 999999)) 
        usr.set_password(password)  # Use set_password for secure password hashing
        usr.save() 

        # Send email notification with the generated password
        send_mail(
            'Student Account Approval',
            f'Your account has been approved. Your temporary password is: {password}',
            settings.EMAIL_HOST_USER,  # Replace with your email settings
            [stud.user.email],  # Send email to the teacher's email
            
        )

    messages.success(request, 'User approved successfully!')
    return redirect('ad')



def disapprove(request, k):
    usr = CustomUser.objects.get(id=k)

    if usr.user_type == '2':
        Teacher.objects.filter(user=usr).delete()
    elif usr.user_type == '3':
        Student.objects.filter(user=usr).delete()

    # Send email notification to the user
    subject = 'Account Disapproval Notification'
    message = 'Your account has been disapproved.'
    from_email = settings.EMAIL_HOST_USER
    to_email = usr.email

    send_mail(subject, message, from_email, [to_email]) 

    usr.delete()
    messages.info(request, 'User disapproved.')
    return redirect('ad')



def resetpassword(request):
    return render (request, 'reset.html')


def reset(request):
    if request.method == 'POST':
        pas = request.POST['new_password']
        cpas = request.POST['confirm_password']

        if pas != cpas:
            messages.error(request, "Passwords don't match")
            return redirect('resetpassword')

        if len(pas) < 6 or not any(char.isupper() for char in pas) \
                or not any(char.isdigit() for char in pas) \
                or not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>/?~' for char in pas):
            messages.error(request, "Password must be at least 6 characters long and contain at least one uppercase letter, one number, and one special character.")
            return redirect('resetpassword')

        else:
            usr = request.user.id
            tsr = CustomUser.objects.get(id=usr)
            tsr.password = pas
            tsr.set_password(pas)
            tsr.save()
            messages.info(request, "Password Changed")
            return redirect('resetpassword')

def logout1(request):
  """Logs out the current user and redirects them to the login page."""
  logout(request)
  return redirect('login1') 