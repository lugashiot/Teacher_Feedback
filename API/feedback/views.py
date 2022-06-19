import sys
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import RatingForm1, RatingForm2, RatingForm3, RatingForm4, RatingForm5, RatingForm6, Textfield_Form
from mail_sender import Mail_Sender
sys.path.append('/home/pi/Feedback/API')
from SQL_Handler import DBHandler
import SQL_Dataclasses as sd

db = DBHandler()
ms = Mail_Sender()


def feedback_page(request):
    if request.method == "GET":
        uuid = request.GET.get("uuid")
        
        # uuid not in query
        if uuid is None:
            return render(request, 'feedback_info_page.html')
        
        # uuid not created
        if uuid not in db.UUIDs.get_all_uuids():
            return render(request, 'error_rocket_page.html', {'error_message': "The UUID is invalid"})

        # uuid used
        if db.UUIDs.is_used(uuid):
            return HttpResponseRedirect('/feedback/uuid_used/')
        
        # uuid unused
        poll_id = db.UUIDs.get_poll_id_by_uuid(uuid)
        poll = sd.Poll(poll_id)  # zB poll_name, poll_questions[0,1,2,3,4,5]
        
        teacher_data = db.Teachers.get_teacher_by_id(poll.teacher_id)
        teacher_name = " ".join([teacher_data.get("Forename"), teacher_data.get("Lastname")])

        rating_1 = RatingForm1(question=sd.Question(poll.poll_question_ids[0]))
        rating_2 = RatingForm2(question=sd.Question(poll.poll_question_ids[1]))
        rating_3 = RatingForm3(question=sd.Question(poll.poll_question_ids[2]))
        rating_4 = RatingForm4(question=sd.Question(poll.poll_question_ids[3]))
        rating_5 = RatingForm5(question=sd.Question(poll.poll_question_ids[4]))
        rating_6 = RatingForm6(question=sd.Question(poll.poll_question_ids[5]))
        text_field = Textfield_Form()
        is_hidden_2, is_hidden_3, is_hidden_4, is_hidden_5, is_hidden_6 = "", "", "", "", ""
        if not rating_2.fields["rating_2"].required: is_hidden_2 = "hidden"        # either hidden or empty
        if not rating_3.fields["rating_3"].required: is_hidden_3 = "hidden"        # either hidden or empty
        if not rating_4.fields["rating_4"].required: is_hidden_4 = "hidden"        # either hidden or empty
        if not rating_5.fields["rating_5"].required: is_hidden_5 = "hidden"        # either hidden or empty
        if not rating_6.fields["rating_6"].required: is_hidden_6 = "hidden"

        return render(request, 'feedback_form_page.html', {'teacher': teacher_name, 'poll_name': poll.poll_name, 'rating_1': rating_1, 'rating_2': rating_2, 'rating_3': rating_3, 'rating_4': rating_4, 'rating_5': rating_5, 'rating_6': rating_6, 'text_field': text_field, 'is_hidden_2': is_hidden_2, 'is_hidden_3': is_hidden_3, 'is_hidden_4': is_hidden_4, 'is_hidden_5': is_hidden_5, 'is_hidden_6': is_hidden_6})

    if request.method == "POST":
        form = RatingForm1(request.POST, question=sd.Question(0))
        data_dict = dict(request.POST)
        
        if not form.is_valid():
            return None

        #getting uuid from link
        whole_url = request.headers['Referer']
        querys = whole_url.split("?")[1]
        if querys.split("=")[0] == "uuid":
            uuid = querys.split("=")[1]
        if uuid not in db.UUIDs.get_all_uuids():
            return render(request, 'error_rocket_page.html', {'error_message': "The UUID is invalid"})
        if db.UUIDs.is_used(uuid):
            return render(request, 'error_rocket_page.html', {'error_message': "You can't vote twice, cheater"})
        
        # TODO 
        # uuid check if "GET" accessed in the last 30 mins?

        answers = [int(data_dict[key][0]) for key in data_dict.keys() if "rating" in key]
        answer_text = "".join([str(data_dict[key][0]) for key in data_dict.keys() if "text_field" in key])

        db.UUIDs.write_answers(uuid, answers, answer_text, datetime.now())
        return HttpResponseRedirect('/feedback/success/')

def uuid_used_page(request):
    return render(request, 'error_rocket_page.html', {'error_message': "The UUID was already used"})

def success_page(request):
    return render(request, 'success_page.html')

def send_mails(request):
    if request.method != "GET":
        return render(request, 'error_rocket_page.html', {'error_message': "HTTP Request was not type GET"})
    
    # Only if it is GET
    input_teacher_username = request.GET.get("teacher")
    input_poll_id = request.GET.get("poll")
    if input_teacher_username == None:
        return render(request, 'error_rocket_page.html', {'error_message': "No Teacher was given"})
    if input_poll_id == None:
        return render(request, 'error_rocket_page.html', {'error_message': "No Poll was given"})
    
    for db_username in db.Teachers.get_all_teachers_username():
        #if teacher exists in database, not if teacher is authenticated
        if db_username == input_teacher_username:       
            teacher_id = db.Teachers.get_teacher_by_username(db_username, "Teacher_ID")
            input_poll = db.Polls.get_poll_by_id(input_poll_id)
            if input_poll == None:
                return render(request, 'error_rocket_page.html', {'error_message': "The Poll given doesn't exist"})
            # if poll creater is not the one sending the mails
            if teacher_id != input_poll[1]:
                return render(request, 'error_rocket_page.html', {'error_message': "This is not your Poll!"})
            
            # if something went wrong at sending the mails
            if not ms.send_emails(input_poll_id, db_username):       
                return render(request, 'error_rocket_page.html', {'error_message': "An Error occured at sending the Emails - Please contact the Administrator to fix your Problem!"})
            
            # if all went well
            break
    return HttpResponseRedirect('/feedback/success/')
