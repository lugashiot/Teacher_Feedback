from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from dataclasses import dataclass, field
from SQL_Handler import DBHandler
from SQL_Dataclasses import *
#from ..SQL_Dataclasses import *

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
            return HttpResponseRedirect('/teacher/login/')
    else:
        return render(request, "account/login.html")


def dashboard(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            username = request.user.username
            teacher_id = db.Teachers.get_teacher_by_username(username, wanted_key="Teacher_ID")
            teacher_polls = db.Polls.get_polls_by_teacher(teacher_id)
            return render(request, "dashboard/dashboard.html", {'polls': teacher_polls})
        else:
            return HttpResponseRedirect('/teacher/login/')


def results(request):
    @dataclass
    class Result:    # results of one question
        question_text: str
        answer_opts: list
        answer_vals: list

    if request.method == "GET":
        if request.user.is_authenticated:
            requested_poll_id = request.GET.get("pid")
            username = request.user.username
            teacher = Teacher(username)

            # todo work with new dataclasses and make html dynamic
            poll_answers = [x.poll_answers for x in teacher.polls if x.poll_id == int(requested_poll_id)][0]
            poll_questions = [x.poll_questions for x in teacher.polls if x.poll_id == int(requested_poll_id)][0]

            all_results=[]
            for i in range(len(poll_questions)):
                all_results.append(Result(question_text=poll_questions[i].question_text, answer_opts=poll_questions[i].question_answer_opts, answer_vals=[x.answers[i] for x in poll_answers]))

            #[i for i in ...] # todo und und dann alle results als 1 liste an html und dann for und in sript dann iterieren aber ka wie (wegen namenvon html div de renamed wean muas)
            #all_results[0].answer_opts
            #[all_results[0].answer_vals.count(i) for i in range(1, 6)]
            return render(request, "dashboard/results.html", {
                # question0
                'q0': "Question0",
                'q0a_opts': all_results[0].answer_opts, 'q0a_vals': [all_results[0].answer_vals.count(i) for i in range(1, 6)],
                # question1
                'q1': "Question1",
                'q1a_opts': all_results[1].answer_opts, 'q1a_vals': [all_results[1].answer_vals.count(i) for i in range(1, 6)],
                # question2
                'q2': "Question2",
                'q2a_opts': all_results[2].answer_opts, 'q2a_vals': [all_results[2].answer_vals.count(i) for i in range(1, 6)],
                # question3
                'q3': "Question3",
                'q3a_opts': all_results[3].answer_opts, 'q3a_vals': [all_results[3].answer_vals.count(i) for i in range(1, 6)],
            })
        else:
            return HttpResponseRedirect('/teacher/login/')


def create_poll(request):
    class QuestionCard:
        def __init__(self, q: str, a: list, btn_name="auto", selected_flag=False):
            self.q = q
            self.a = a
            self.selected_flag = selected_flag
            if btn_name == "auto":
                if questions_temp:
                    self.btn_name = str(max([int(x.btn_name) for x in questions_temp]) + 1)
                else:
                    self.btn_name = "0"
            else:
                self.btn_name = btn_name

        def check_if_filled_correctly(self):
            if self.q != "" and "" not in self.a and self.btn_name != "":
                return True
            return False

    def return_(error_msg=""):
        return render(request, "dashboard/create_poll.html", {'questions': [x for x in questions_temp if x.selected_flag is False], 'questions_selected': [x for x in questions_temp if x.selected_flag is True], 'poll_name': "MTRS 3. und 4. Klasse", 'error': error_msg})  # todo richtige klasse übergeben

    def update_questions_from_db(usr):
        teacher = Teacher(usr)
        return [QuestionCard(teacher.questions[i].question_text, teacher.questions[i].question_answer_opts) for i in range(len(teacher.questions))]

    if request.user.is_authenticated:
        username = request.user.username
        #questions_temp = [QuestionCard(x.question_text, x.question_answer_opts, str(x.question_id)) for x in [Question(i) for i in db.Questions.get_public_questions() if i != 0]] # todo load default questions
        questions_temp = []
        questions_temp = update_questions_from_db(username)
        if request.method == "GET":

            return return_()

        elif request.method == "POST":
            for btn in [q.btn_name for q in questions_temp]:
                if btn in request.POST:
                    if request.POST[btn] == "Hinzufügen":
                        if len([x for x in questions_temp if x.selected_flag is True]) < 6:
                            [x for x in questions_temp if x.btn_name == btn][0].selected_flag = True
                            return return_()
                        else:
                            return return_("Sie können nur 6 Fragen auswählen!")
                    elif request.POST[btn] == "Entfernen":
                        for i in [x for x in questions_temp if x.selected_flag is True and x.btn_name == btn]:
                            i.selected_flag = False
                        return return_()

            if "q_inp" in request.POST:
                new_question = QuestionCard(request.POST["q_inp"], [request.POST["a0_inp"], request.POST["a1_inp"], request.POST["a2_inp"], request.POST["a3_inp"], request.POST["a4_inp"]], "auto")
                if new_question.check_if_filled_correctly():
                    if new_question.q not in [x.q for x in questions_temp]:
                        db.Questions.write_question(db.Teachers.get_teacher_by_username(username, "Teacher_ID"), new_question.q, new_question.a, 0)
                        questions_temp = update_questions_from_db(username)
                        return return_()
                    else:
                        return return_("Diese Frage existiert leider schon!")
                else:
                    return return_("Frage nicht gültig!")
        return return_(str(request.POST))
    else:
        return HttpResponseRedirect('/teacher/login/')


def redirect_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/teacher/dashboard/')
    else:
        return HttpResponseRedirect('/teacher/login/')
