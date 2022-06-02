import uuid
from datetime import datetime
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configparser

config = configparser.ConfigParser()
# config.read("config.ini")           # for pi
config.read("../../config.ini")     # for pc


class EmailHandler:
    def __init__(self) -> None:
        self.user = config["email"]["address"]
        self.password = config["email"]["password"]
        self.server = config["email"]["server"]

    def build_email(self, send_to, uuid, teacher: str):
        teacher_no_dot = teacher.replace(".", " ")
        msg = MIMEMultipart("alternative")
        msg['Subject'] = f"Feedback für {teacher_no_dot}"
        msg['From'] = "HTL-Feedback-Bot@htlinn.tech"
        msg['To'] = send_to
        msg['Date'] = datetime.now().ctime()

        # file = open("API/feedback/templates/student_email_content.html", "r")   # for pi
        file = open("templates/student_email_content.html", "r")                # for pc

        ue = u"\u00FC"
        oe = u"\u00F6"
        copyright = u"\u00A9"
        student = str(send_to).split("@")[0]
        curved_bracket_open = u"{"
        curved_bracket_close = u"}"

        part1 = MIMEText(file.read().format(ue=ue, oe=oe, uuid=uuid, copyright=copyright, student=student, teacher=teacher_no_dot, curved_bracket_open=curved_bracket_open, curved_bracket_close=curved_bracket_close), "html", "utf-8")

        msg.attach(part1)

        # msg.add_header('Content-Type', 'text/html')
        # file = open("templates/student_email_content.html", "r")
        # msg.set_payload(file.read())

        return msg


class Class:
    def __init__(self, name) -> None:
        self.name = name
        self.students = []
        self.load_students()

    def load_students(self):
        f = None
        try:
            f = open(f"{self.name}.txt", "r").read()
        except:
            try:
                f = open(f"API/feedback/{self.name}.txt", "r").read()
            except:
                print("ERROR: Couldn't load students")
        emails = f.split(",")
        self.students = emails

    # Do NOT run this method itself, only run the Teacher.send_emails()
    def send_emails(self, teacher) -> dict:
        temp_uuid_list = []
        temp_dict = {
            "class": self.name,
            "teacher": teacher,
            "uuid_list": []
        }
        email_handler = EmailHandler()
        with SMTP(email_handler.server) as server:
            server.login(email_handler.user, email_handler.password)
            for student_email in self.students:
                id = uuid.uuid4()
                msg = email_handler.build_email(student_email, id, teacher)
                server.sendmail(email_handler.user, msg['To'], msg.as_string())  # sent from, send to, email text
                temp_uuid_list.append(id)
                print(f"Feedback link to {student_email} was sent! UUID: {id}")
            temp_dict["uuid_list"] = temp_uuid_list
        print(f"All emails to class {self.name} were sent by {teacher}!")

        return temp_dict


class Teacher:
    def __init__(self, username) -> None:
        self.forename = ""
        self.lastname = ""
        self.username = username
        self.classes = []

    def add_class(self, temp_class: Class):
        self.classes.append(temp_class)

    def send_emails(self, classname="all"):
        if classname == "all":
            for c in self.classes:
                c.send_emails(self.username)
                print("saved dict somewhere lol")
            print(f"All Emails to all classes of {self.username} were sent!")
            return True
        for c in self.classes:
            if c.name == classname:
                c.send_emails(self.username)
                print("saved dict somewhere lol")
                print(f"All Emails to {classname} were sent!")
                return True
        return False


if __name__ == "__main__":
    input("Start Test: Press Enter")
    class1 = Class("4CHEL")
    teacher1 = Teacher("Gilbert.Senn")
    teacher1.add_class(class1)
    #teacher1.send_emails()
    teacher1.send_emails(classname=class1.name)
