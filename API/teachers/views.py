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
            return HttpResponseRedirect('/teacher/login/')
    else:
        return render(request, "account/login.html")


def dashboard(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            username = request.user.username
            teacher_id = db.get_teacher_by_username(username, wanted_key="Teacher_ID")
            teacher_classes = db.get_class_assignments(teacher_id)
            return render(request, "dashboard/dashboard.html", {'classes': teacher_classes})
        else:
            return HttpResponseRedirect('/teacher/login/')


def results(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            requested_class = request.GET.get("class")
            username = request.user.username
            teacher_id = db.get_teacher_by_username(username, wanted_key="Teacher_ID")
            teacher_classes = db.get_class_assignments(teacher_id)
            if requested_class in teacher_classes:
                class_answers = db.get_answers_for_class(teacher_id, requested_class)

                all_results = [[], [], [], []]
                for answer in class_answers:
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
    def __init__(self, q, a0, a1, a2, a3, a4):
        self.q = q
        self.a0 = a0
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        self.a4 = a4

    def check_if_filled_correctly(self):
        if self.q is not "" and self.a0 is not "" and self.a1 is not "" and self.a2 is not "" and self.a3 is not "" and self.a4 is not "":
            return True
        return False


def create_poll(request):
    questions_temp = [
        Question("Test Frage 1  long fucking text", "ok  lol lel saaaaassss", "ok", "ok", "okkkkkkkkkkkk", "ok"),
        Question("Test Frage 2  long fucking text", "ok  lol lel saaaaassss", "ok", "ok", "okkkkkkkkkkkk", "ok"),
        Question("Test Frage 3  long fucking text", "ok  lol lel saaaaassss", "ok", "ok", "okkkkkkkkkkkk", "ok"),
        Question("Test Frage 4  long fucking text", "ok  lol lel saaaaassss", "ok", "ok", "okkkkkkkkkkkk", "ok"),
        Question("Test Frage 5  long fucking text", "ok  lol lel saaaaassss", "ok", "ok", "okkkkkkkkkkkk", "ok"), ]

    if request.method == "GET":
        if request.user.is_authenticated:
            username = request.user.username
            teacher_id = db.get_teacher_by_username(username, wanted_key="Teacher_ID")
            teacher_classes = db.get_class_assignments(teacher_id)

            #return render(request, "dashboard/create_poll.html", {'questions': db.load_questions_for_teacher(...)})    # todo load premade questions
            return render(request, "dashboard/create_poll.html", {'questions': questions_temp, 'class': "4CHEL"})   # todo richtige klasse übergeben
        else:
            return HttpResponseRedirect('/teacher/login/')

    if request.method == "POST":
        if "q_inp" in request.POST:
            new_question = Question(request.POST["q_inp"], request.POST["a0_inp"], request.POST["a1_inp"], request.POST["a2_inp"], request.POST["a3_inp"], request.POST["a4_inp"])
            if new_question.check_if_filled_correctly():
                if new_question.q not in [a.q for a in questions_temp]:
                    questions_temp.append(new_question)
                return render(request, "dashboard/create_poll.html", {'questions': questions_temp, 'class': "4CHEL"})   # todo richtige klasse übergeben
            else:
                return HttpResponseRedirect('/')    # todo push error message


def redirect_login(request):
    return HttpResponseRedirect('/teacher/login/')
