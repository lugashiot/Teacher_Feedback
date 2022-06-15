from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from SQL_Handler import DBHandler
from SQL_Dataclasses import *
from ..SQL_Dataclasses import *

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
    if request.method == "GET":
        if request.user.is_authenticated:
            requested_poll_id = request.GET.get("poll_id")
            username = request.user.username
            teacher_id = db.Teachers.get_teacher_by_username(username, wanted_key="Teacher_ID")
            teacher_polls = db.Polls.get_polls_by_teacher(teacher_id)

            # Poll_ID, Teacher_ID, Poll_Name, Ass_1, Ass_2, Ass_3, Ass_4, Ass_5, Q_ID_1, Q_ID_2, Q_ID_3, Q_ID_4, Q_ID_5, Q_ID_6, Poll_Time
            # Question_ID, Question_Text, Ans_Opt_1, Ans_Opt_2, Ans_Opt_3, Ans_Opt_4, Ans_Opt_5, Teacher_ID

            if requested_poll_id in [x[1] for x in teacher_polls]:
                question_data = db.Questions.get_questions_by_id(requested_poll_id)
                question_answers = question_data[2]
                question_title = question_data[1]
                question_id = question_data[1]

                # Question_ID, Question_Text, Ans_Opt_1, Ans_Opt_2, Ans_Opt_3, Ans_Opt_4, Ans_Opt_5, Teacher_ID

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


class Question:
    def __init__(self, q: str, a: list,  btn_name="auto", selected_flag=False):
        self.q = q
        self.a = a
        self.selected_flag = selected_flag
        if btn_name == "auto":
            self.btn_name = str(int([q.btn_name for q in questions_temp][-1])+1)
        else:
            self.btn_name = btn_name

    def check_if_filled_correctly(self):
        if self.q != "" and "" not in self.a and self.btn_name != "":
            return True
        return False


questions_temp = [
    Question("Wie gut findest du den Unterricht von dieser Lehrperson?", ["sehr gut", "gut", "ok", "weniger gut", "nicht gut"], "0"),
    Question("Wie gut kommst du im Unterricht von dieser Lehrperson mit?", ["sehr leicht verständlich", "gut verständlich", "verständlich", "schwer verständlich", "nicht verständlich"], "1"),
    Question("Wie verständlich ist der im Unterricht behandelte Stoff?", ["sehr gering", "gering", "akzeptabel", "übermäßig", "zu viel"], "2"),
    Question("Wie hoch ist dein (Zeit-)Aufwand zuhause um im Unterricht dabei zu bleiben? (Lernen + Hü)", ["ok", "ok", "ok", "ok", "ok"], "3")]
questions_selected = []   # todo database shit für des


def create_poll(request):
    def return_(error_msg=""):
        return render(request, "dashboard/create_poll.html", {'questions': [x for x in questions_temp if x.selected_flag == False], 'questions_selected': questions_selected, 'poll_name': "MTRS 3. und 4. Klasse", 'error': error_msg})  # todo richtige klasse übergeben

    if request.user.is_authenticated:
        username = request.user.username
        if request.method == "GET":

            return return_()

        elif request.method == "POST":
            teacher = Teacher(username)

            for btn in [q.btn_name for q in questions_temp]:
                if btn in request.POST:
                    if request.POST[btn] == "Hinzufügen":
                        if len([x for x in questions_temp if x.selected_flag is True]) < 6:
                            [x for x in questions_temp if x.btn_name == btn][0].selected_flag = True
                            return return_()
                        else:
                            return return_("Sie können nur 6 Fragen auswählen!")
                    elif request.POST[btn] == "Entfernen":
                        [x for x in questions_temp if x.selected_flag is True and x.btn_name == btn][0].selected_flag = False
                        return return_()

            if "q_inp" in request.POST:
                new_question = Question(request.POST["q_inp"], [request.POST["a0_inp"], request.POST["a1_inp"], request.POST["a2_inp"], request.POST["a3_inp"], request.POST["a4_inp"]], "auto")
                if new_question.check_if_filled_correctly():
                    if new_question.q not in [a.q for a in questions_temp]:
                        questions_temp.append(new_question)     # in db für fragen eintragen (private)
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
