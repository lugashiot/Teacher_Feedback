from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.contrib import messages
from dataclasses import dataclass, field
from SQL_Handler import DBHandler
from SQL_Dataclasses import *
from mail_sender import Mail_Sender

#from ..SQL_Dataclasses import *

db = DBHandler()
ms = Mail_Sender()


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


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        cards.clear()
    return HttpResponseRedirect('/teacher/login/')


def dashboard(request):
    def badge_color(value: float):
        if value >= 0.75:
            return "success"
        if value >= 0.25:
            return "warning"
        return "danger"
    
    if request.method != "GET":
        return HttpResponseRedirect('/teacher/login/')
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/teacher/login/')
    if request.user.is_superuser:
        return HttpResponseRedirect('/teacher/management/')

    username = request.user.username
    teacher = Teacher(username)

    return render(request, "dashboard/dashboard.html", {'polls': [[x.poll_id, x.poll_name, len([y for y in x.poll_answers if y.answers[0] != 0]), len(x.poll_answers), badge_color(len([y for y in x.poll_answers if y.answers[0] != 0])/len(x.poll_answers))] for x in teacher.polls]})


def results(request):
    @dataclass
    class Result:
        question_text: str
        answer_opts: list[str]
        answer_vals: list[int]

    if not request.user.is_authenticated:
        return HttpResponseRedirect('/teacher/login/')
    username = request.user.username
    teacher = Teacher(username)
    if request.method == "GET":
        requested_poll_id = int(request.GET.get("pid"))
        if requested_poll_id not in [x.poll_id for x in teacher.polls]:
            return render(request, 'error_rocket_page.html', {'error_message': "Diese Umfrage existiert leider nicht"})

        poll_name = [x.poll_name for x in teacher.polls if x.poll_id == requested_poll_id][0]
        poll_answers = [x.poll_answers for x in teacher.polls if x.poll_id == requested_poll_id][0]
        poll_questions = [x.poll_questions for x in teacher.polls if x.poll_id == requested_poll_id][0]

        all_results = []
        for i in range(6):
            try:
                all_results.append(Result(question_text=poll_questions[i].question_text,
                                          answer_opts=poll_questions[i].question_answer_opts,
                                          answer_vals=[x.answers[i] for x in poll_answers]))
            except IndexError as e:
                all_results.append(
                    Result(question_text="-", answer_opts=["-", "-", "-", "-", "-"], answer_vals=[0, 0, 0, 0, 0]))

        return render(request, "dashboard/results.html", {
            'poll_name': poll_name,
            'hidden_flags_list': [False] * len(poll_questions) + [True] * (6 - len(poll_questions)),
            # question0
            'q0': all_results[0].question_text,
            'q0a_opts': all_results[0].answer_opts,
            'q0a_vals': [all_results[0].answer_vals.count(i) for i in range(1, 6)],
            # question1
            'q1': all_results[1].question_text,
            'q1a_opts': all_results[1].answer_opts,
            'q1a_vals': [all_results[1].answer_vals.count(i) for i in range(1, 6)],
            # question2
            'q2': all_results[2].question_text,
            'q2a_opts': all_results[2].answer_opts,
            'q2a_vals': [all_results[2].answer_vals.count(i) for i in range(1, 6)],
            # question3
            'q3': all_results[3].question_text,
            'q3a_opts': all_results[3].answer_opts,
            'q3a_vals': [all_results[3].answer_vals.count(i) for i in range(1, 6)],
            # question4
            'q4': all_results[4].question_text,
            'q4a_opts': all_results[4].answer_opts,
            'q4a_vals': [all_results[4].answer_vals.count(i) for i in range(1, 6)],
            # question5
            'q5': all_results[5].question_text,
            'q5a_opts': all_results[5].answer_opts,
            'q5a_vals': [all_results[5].answer_vals.count(i) for i in range(1, 6)],
            # textinput
            'texts': [x.feedback_text for x in poll_answers if x.feedback_text != 'None' and x.feedback_text != ""]
        })

    elif request.method == "POST":
        requested_poll_id = int(request.GET.get("pid"))
        db.Polls.delete_poll_recursive(requested_poll_id)
        return HttpResponseRedirect('/teacher/dashboard/')


def management(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/teacher/login/')
    if not request.user.is_superuser:
        return HttpResponseRedirect('/teacher/dashboard/')

    teachers = []
    for t in db.Teachers.get_all_teachers_username():
        teachers.append(Teacher(t))

    if request.method != "POST":
        return render(request, "dashboard/management.html", {'teachers': teachers})

    danger_operations = ["Alle Lehrer l??schen", "Alle Sch??ler l??schen", "Alle Umfragen l??schen", "Alle benutzerdefinierten Fragen l??schen"]
    if "danger_btn_inp" in request.POST and request.POST["danger_btn_inp"] in danger_operations:
        msg = f"Um zu best??tigen dass Sie \"{ request.POST['danger_btn_inp'] }\" m??chten, geben Sie diesen Text ein."
        operation = request.POST['danger_btn_inp']
        return render(request, "dashboard/management.html", {'successful_submit': True, 'confirmation': True, 'msg': msg, 'operation': operation, 'teachers': teachers})
    elif "danger_confirm_btn_inp" in request.POST and "confirmation" in request.POST and request.POST["danger_confirm_btn_inp"] in danger_operations:
        if request.POST["danger_confirm_btn_inp"] == request.POST["confirmation"]:
            # todo alles confirmed operation soll durchgef??hrt werden
            if request.POST["danger_confirm_btn_inp"] == danger_operations[0]:
                pass
            elif request.POST["danger_confirm_btn_inp"] == danger_operations[1]:
                pass
            elif request.POST["danger_confirm_btn_inp"] == danger_operations[2]:
                pass
            elif request.POST["danger_confirm_btn_inp"] == danger_operations[3]:
                pass
            msg = f"Operation \"{request.POST['danger_confirm_btn_inp']}\" erfolgreich ausgef??hrt"
            operation = request.POST['danger_confirm_btn_inp']
            return render(request, "dashboard/management.html", {'successful_submit': True, 'confirmation': False, 'msg': msg, 'operation': operation, 'teachers': teachers})
    elif "parse_student_list" in request.POST:
        pass

    # ab da is da user angemeldet, superuser und hat auf an button probably druckt
    return None


class QuestionCard:
    def __init__(self, q: str, a: list, btn_name: int, selected_flag=False):
        self.q = q
        self.a = a
        self.btn_name = btn_name
        self.selected_flag = selected_flag

    def check_if_filled_correctly(self):
        if self.q != "" and "" not in self.a and self.btn_name != "":
            return True
        return False


class Cards:
    def __init__(self):
        self.question_cards = []

    def add_card(self, card: QuestionCard):
        self.question_cards.append(card)

    def clear(self):
        self.question_cards.clear()


cards = Cards()


def create_poll(request):
    def return_(error_msg="", success_msg=""):
        return render(request, "dashboard/create_poll.html",
                      {'questions': [x for x in cards.question_cards if x.selected_flag is False],
                       'questions_selected': [x for x in cards.question_cards if x.selected_flag is True],
                       'teacher_assignments': teacher.assignments,
                       'error': error_msg,
                       'success': success_msg})

    def update_questions_from_db(usr):
        teacher = Teacher(usr)
        default_questions = [Question(id) for id in [1, 2, 3, 4]]
        for q in default_questions:
            if q.question_id not in [x.btn_name for x in cards.question_cards]:
                cards.add_card(QuestionCard(q.question_text, q.question_answer_opts, q.question_id))
        for q in teacher.questions:
            if q.question_id not in [x.btn_name for x in cards.question_cards]:
                cards.add_card(QuestionCard(q.question_text, q.question_answer_opts, q.question_id))

    if request.user.is_authenticated:
        username = request.user.username
        teacher = Teacher(username)
        update_questions_from_db(username)
        if request.method == "GET":
            return return_()

        elif request.method == "POST":
            if "q_inp" in request.POST:
                q = request.POST["q_inp"]
                a = [request.POST["a0_inp"], request.POST["a1_inp"], request.POST["a2_inp"], request.POST["a3_inp"],
                     request.POST["a4_inp"]]
                if q != "" and "" not in a:
                    if q not in [x.q for x in cards.question_cards]:
                        db.Questions.write_question(db.Teachers.get_teacher_by_username(username, "Teacher_ID"), q, a,
                                                    0)
                        update_questions_from_db(username)
                        return return_()
                    else:
                        return return_(error_msg="Diese Frage existiert leider schon!")
                else:
                    return return_(error_msg="Frage nicht g??ltig!")
            elif "send_poll" in request.POST:
                if request.POST["poll_name_inp"] in [x.poll_name for x in teacher.polls]:
                    return return_(error_msg="Sie haben bereits eine Umfrage die so hei??t!")
                if len(request.POST["poll_name_inp"]) < 5:  # name der Umfrage muss 5 zeichen lang sein
                    return return_(error_msg="Der Name der Umfrage muss mindestens 5 Zeichen lang sein!")
                requested_assignments = [x for x in teacher.assignments if x in request.POST][0:5]
                if len(requested_assignments) == 0:
                    return return_(error_msg="Sie m??ssen eine oder mehrere Klasse ausw??hlen!")
                if len(requested_assignments) > 5:
                    return return_(error_msg="Sie k??nnen maximal 5 Klassen ausw??hlen!")
                requested_assignment_ids = [db.Teachers_Assignments.get_assignment_id(teacher.teacher_id, x) for x in
                                            requested_assignments]
                requested_assignment_ids += [0] * (5 - len(requested_assignments))

                question_ids = [int(x.btn_name) for x in cards.question_cards if x.selected_flag is True][0:6]
                question_ids += [0] * (6 - len(question_ids))

                db.Polls.write_poll(teacher.teacher_id, request.POST["poll_name_inp"], requested_assignment_ids[0],
                                    requested_assignment_ids[1], requested_assignment_ids[2],
                                    requested_assignment_ids[3], requested_assignment_ids[4], question_ids[0],
                                    question_ids[1], question_ids[2], question_ids[3], question_ids[4], question_ids[5])
                for q in cards.question_cards:
                    q.selected_flag = False

                poll_id = db.Polls.get_poll_id_by_arguments(teacher.teacher_id, request.POST["poll_name_inp"])
                if ms.send_emails(poll_id, teacher.teacher_username):
                    return return_(success_msg=f"Umfrage erfolgreich an {', '.join(requested_assignments)} gesendet. "
                                               f"Um die Ergebnisse anzusehen klicken Sie <a href='/teacher/dashboard/results/?pid={poll_id}' class='alert-link'>hier</a>.")
                return return_(error_msg="Fehler beim Senden der Mails aufgetreten")

            elif [x for x in (teacher.questions + [Question(id) for id in [1, 2, 3, 4]]) if str(x.question_id) in request.POST]:
                card = [x for x in cards.question_cards if str(x.btn_name) in request.POST][0]
                if request.POST[str(card.btn_name)] == "Hinzuf??gen":
                    if len([x for x in cards.question_cards if x.selected_flag is True]) < 6:
                        card.selected_flag = True
                        return return_()
                    else:
                        return return_(error_msg="Sie k??nnen nur 6 Fragen ausw??hlen!")
                elif request.POST[str(card.btn_name)] == "Entfernen":
                    card.selected_flag = False
                    return return_()
                elif request.POST[str(card.btn_name)] == "L??schen":
                    db.Questions.delete_teacher_from_question(card.btn_name)
                    cards.question_cards.pop(cards.question_cards.index(card))
                    return return_()
            else:
                return return_(error_msg="Auswahl nicht erkannt!")
        return return_(str(request.POST))
    else:
        return HttpResponseRedirect('/teacher/login/')


def redirect_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/teacher/dashboard/')
    else:
        return HttpResponseRedirect('/teacher/login/')
