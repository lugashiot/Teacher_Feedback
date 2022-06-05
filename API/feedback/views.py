import os, sys
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import RatingForm1, RatingForm2, RatingForm3, RatingForm4
from . import mail_sender as MS
sys.path.append('/home/pi/Feedback/API')
from SQL_Handler import DBHandler


class1 = MS.Class("4CHEL")
teacher1 = MS.Teacher("Gilbert.Senn")
teacher1.add_class(class1)
Handle = DBHandler()

def feedback_page(request):
    if request.method == "GET":
        uuid = request.GET.get("uuid")
        
        #uuid not in query
        if uuid is None:
            return render(request, 'feedback_info_page.html')
        
        #uuid not created
        if uuid not in Handle.get_all_uuids():
            return render(request, 'error_rocket_page.html', {'error_message': "The UUID is invalid"})

        #uuid used
        if Handle.is_uuid_used(uuid):
            return HttpResponseRedirect('/feedback/uuid_used/')
        
        #uuid unused
        teacher_id = Handle.get_teacher_id_by_uuid(uuid)
        temp_teacher = Handle.get_teacher_by_id(teacher_id)
        teacher_name = temp_teacher["Forename"] + " " + temp_teacher["Lastname"]
        rating_1 = RatingForm1()
        rating_2 = RatingForm2()
        rating_3 = RatingForm3()
        rating_4 = RatingForm4()
        return render(request, 'feedback_form_page.html', {'uuid': uuid, 'teacher': teacher_name, 'rating_1': rating_1, 'rating_2': rating_2, 'rating_3': rating_3, 'rating_4': rating_4})

    if request.method == "POST":
        form = RatingForm1(request.POST)
        data_dict = dict(request.POST)
        Answers = []
        if form.is_valid():
            whole_url = request.headers['Referer']
            querys = whole_url.split("?")[1]
            if querys.split("=")[0] == "uuid":
                uuid = querys.split("=")[1]

            for key in data_dict.keys():
                if "rating" in key:
                    value = int(data_dict[key][0])
                    Answers.append(str(value))
            
            if Handle.is_uuid_used(uuid):
                return render(request, 'error_rocket_page.html', {'error_message': "You can't vote twice, cheater"})
            Handle.write_answers(uuid, Answers[0], Answers[1], Answers[2], Answers[3])
            return HttpResponseRedirect('/feedback/success/')

def uuid_used_page(request):
    return render(request, 'error_rocket_page.html', {'error_message': "The UUID was already used"})

def success_page(request):
    return render(request, 'success_page.html')

def send_mails(request):
    def create_backend():
        class_list = Handle.get_class_assignments(Handle.get_teacher_by_username(username, "Teacher_ID"))
        temp_teacher = MS.Teacher(username)
        for school_class in class_list:
            temp_teacher.add_class(MS.Class(school_class))
        return temp_teacher
    
    flag = False
    if request.method == "GET":
        input_teacher = request.GET.get("teacher")
        input_class = request.GET.get("class")
        if input_teacher is None:
            return render(request, 'error_rocket_page.html', {'error_message':"No Teacher was given"})
        if input_class is None:
            input_class = "all"
        for username in Handle.get_all_teachers_username():
            if username == input_teacher:
                teacher = create_backend()
                flag = teacher.send_emails(input_class)
        if not flag:
            return render(request, 'error_rocket_page.html', {'error_message': input_teacher + ";" + input_class})
            return render(request, 'error_rocket_page.html', {'error_message': "Either the Teacher given doesn't exist, or something else went wrong at sending the mails."})
        return HttpResponseRedirect('/feedback/success/')
    return render(request, 'error_rocket_page.html', {'error_message': "HTTP Request was not type GET"})

