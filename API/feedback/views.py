import os

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import RatingForm1, RatingForm2, RatingForm3, RatingForm4
from .mail_sender import Class, Teacher


uuid_used = []
uuid_created = []
class1 = Class("4CHEL")
teacher1 = Teacher("Gilbert.Senn")
teacher1.add_class(class1)
teachers = [teacher1]


def feedback_page(request):
    if request.method == "GET":
        uuid = request.GET.get("uuid")
        
        #uuid not in query
        if uuid is None:
            return render(request, 'feedback_info_page.html')
        
        #uuid not created
        #if uuid not in uuid_created:
        #    return render(request, 'error_page.html', {'error_message': "UUID is invalid / was not created"})

        #uuid used
        if uuid in uuid_used:
            return HttpResponseRedirect('/feedback/uuid_used/')
        
        #uuid unused
        teacher = "Gilbert.Senn"
        rating_1 = RatingForm1()
        rating_2 = RatingForm2()
        rating_3 = RatingForm3()
        rating_4 = RatingForm4()
        return render(request, 'feedback_form_page.html', {'uuid': uuid, 'teacher': teacher, 'rating_1': rating_1, 'rating_2': rating_2, 'rating_3': rating_3, 'rating_4': rating_4})

    if request.method == "POST":
        form = RatingForm1(request.POST)
        
        data_dict = dict(request.POST)
        for key in data_dict.keys():
            if "rating" in key:
                value = int(data_dict[key][0])
                try:
                    print(f"{key} : {value}")
                except:
                    pass
        
        if form.is_valid():
            whole_url = request.headers['Referer']
            querys = whole_url.split("?")[1]
            if querys.split("=")[0] == "uuid":
                uuid = querys.split("=")[1]
                uuid_used.append(uuid)
            return HttpResponseRedirect('/feedback/success/')

def uuid_used_page(request):
    return render(request, 'error_rocket_page.html', {'error_message': "The UUID was already used"})

def success_page(request):
    return render(request, 'success_page.html')

def send_mails(request):
    flag = False
    if request.method == "GET":
        teacher = request.GET.get("teacher")
        classes = request.GET.get("class")
        if teacher is None:
            return render(request, 'error_rocket_page.html', {'error_message':"No Teacher was given"})
        if classes is None:
            classes = "all"
        
        for t in teachers:
            if t.username == teacher:
                sent = t.send_emails(classes)
                flag = True
                if not sent:
                    flag = False
            if not flag:   
                return render(request, 'error_rocket_page.html', {'error_message': "Either the Teacher given doesn't exist, or something else went wrong at sending the mails."})
        return HttpResponseRedirect('/feedback/success/')
    return render(request, 'error_rocket_page.html', {'error_message': "HTTP Request was not type GET"})

