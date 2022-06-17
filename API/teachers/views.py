from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from SQL_Handler import DBHandler
from SQL_Dataclasses import *
from ..SQL_Dataclasses import *

db = DBHandler()


def login_user(request):
    if request.method != "POST":
        return render(request, "account/login.html")
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is None:
        messages.success(request, "There was an error logging in, try again...")
        return HttpResponseRedirect('/teacher/login/')
    login(request, user)
    return HttpResponseRedirect("/teacher/dashboard")


def dashboard(request):
    if request.method != "GET":
        return HttpResponseRedirect('/teacher/login/')
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/teacher/login/')
    username = request.user.username
    teacher_id = db.Teachers.get_teacher_by_username(username, wanted_key="Teacher_ID")
    teacher_polls = db.Polls.get_polls_by_teacher(teacher_id)
    return render(request, "dashboard/dashboard.html", {'polls': teacher_polls})


def results(request):
    class Result:
        def __int__(self, q: str, a_opts: list, a_vals=[]):
            self.q = q
            self.a_opts = a_opts
            self.a_vals = a_vals

        def get_a_vals_from_list(self, result_list: list):
            for i in range(1, 6):
                self.a_vals.append(result_list.count(i))

    if request.method == "GET":
        if request.user.is_authenticated:
            requested_poll_id = request.GET.get("poll_id")
            username = request.user.username
            teacher_id = db.Teachers.get_teacher_by_username(username, wanted_key="Teacher_ID")
            teacher_polls = db.Polls.get_polls_by_teacher(teacher_id)

            if requested_poll_id in [x[1] for x in teacher_polls]:
                question_data = db.Questions.get_questions_by_id(requested_poll_id)
                question_answers = question_data[2]
                question_title = question_data[1]
                question_id = question_data[1]

                all_results = [[], [], [], []]
                for answer in poll_answers:
                    for i in range(len(all_results)):
                        all_results[i].append(answer[i])

                return render(request, "dashboard/results.html", {
                    # question0
                    'q0': "Question0",
                    'q0a0': "q0a0_test", 'q0a0_val': all_results[0].count(1),
                    'q0a1': "q0a1_test", 'q0a1_val': all_results[0].count(2),
                    'q0a2': "q0a2_test", 'q0a2_val': all_results[0].count(3),
                    'q0a3': "q0a3_test", 'q0a3_val': all_results[0].count(4),
                    'q0a4': "q0a4_test", 'q0a4_val': all_results[0].count(5),
                    # question1
                    'q1': "Question1",
                    'q1a0': "q1a0_test", 'q1a0_val': all_results[1].count(1),
                    'q1a1': "q1a1_test", 'q1a1_val': all_results[1].count(2),
                    'q1a2': "q1a2_test", 'q1a2_val': all_results[1].count(3),
                    'q1a3': "q1a3_test", 'q1a3_val': all_results[1].count(4),
                    'q1a4': "q1a4_test", 'q1a4_val': all_results[1].count(5),
                    # question2
                    'q2': "Question2",
                    'q2a0': "q2a0_test", 'q2a0_val': all_results[2].count(1),
                    'q2a1': "q2a1_test", 'q2a1_val': all_results[2].count(2),
                    'q2a2': "q2a2_test", 'q2a2_val': all_results[2].count(3),
                    'q2a3': "q2a3_test", 'q2a3_val': all_results[2].count(4),
                    'q2a4': "q2a4_test", 'q2a4_val': all_results[2].count(5),
                    # question3
                    'q3': "Question3",
                    'q3a0': "q3a0_test", 'q3a0_val': all_results[3].count(1),
                    'q3a1': "q3a1_test", 'q3a1_val': all_results[3].count(2),
                    'q3a2': "q3a2_test", 'q3a2_val': all_results[3].count(3),
                    'q3a3': "q3a3_test", 'q3a3_val': all_results[3].count(4),
                    'q3a4': "q3a4_test", 'q3a4_val': all_results[3].count(5),
                })
            else:
                return HttpResponseRedirect('/teacher/dashboard/')
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
