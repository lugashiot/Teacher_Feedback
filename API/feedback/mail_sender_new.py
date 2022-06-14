import os, uuid, sys
from datetime import datetime
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configparser

config = configparser.ConfigParser()


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

        file = open(student_email_content_path, "r")

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



if __name__ == "__main__":      # for testing on pc
    sys.path.append(os.path.split(os.getcwd())[0])
    from SQL_Handler import DBHandler
    db = DBHandler()
    
    input("Start Test: Press Enter")
    config.read("../../config.ini")
    student_email_content_path = "templates/student_email_content.html"

