from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from SQL_Handler import DBHandler

db = DBHandler()


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/teacher/dashboard")
        else:
            messages.success(request, "There was an error logging in, try again...")
            return HttpResponseRedirect('/teacher/login_user/')
    else:
        return render(request, "registration/login.html")


def dashboard(request):
    if request.user.is_authenticated:
        username = request.user.username
        teacher_id = db.get_teacher_by_username(username, wanted_key="Teacher_ID")
        teacher_classes = db.get_class_assignments(teacher_id)
        return render(request, "dashboard/dashboard.html", {'classes': teacher_classes})


def results(request):
    return render(request, "dashboard/results.html", {
        # question0
        'q0': "Question0",
        'q0a0': "q0a0", 'q0a0_val': 8,
        'q0a1': "q0a1", 'q0a1_val': 2,
        'q0a2': "q0a2", 'q0a2_val': 3,
        'q0a3': "q0a3", 'q0a3_val': 1,
        # question1
        'q1': "Question1",
        'q1a0': "q1a0", 'q1a0_val': 4,
        'q1a1': "q1a1", 'q1a1_val': 7,
        'q1a2': "q1a2", 'q1a2_val': 2,
        'q1a3': "q1a3", 'q1a3_val': 1,
        # question2
        'q2': "Question2",
        'q2a0': "q2a0", 'q2a0_val': 0,
        'q2a1': "q2a1", 'q2a1_val': 4,
        'q2a2': "q2a2", 'q2a2_val': 7,
        'q2a3': "q2a3", 'q2a3_val': 1,
        # question3
        'q3': "Question3",
        'q3a0': "q3a0", 'q3a0_val': 0,
        'q3a1': "q3a1", 'q3a1_val': 0,
        'q3a2': "q3a2", 'q3a2_val': 0,
        'q3a3': "q3a3", 'q3a3_val': 10,
    })


def redirect_login(request):
    return HttpResponseRedirect('/teacher/login/')
