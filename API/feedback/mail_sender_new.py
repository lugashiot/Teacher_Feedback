import os, uuid, sys
from datetime import datetime
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configparser
sys.path.append(os.path.split(os.getcwd())[0])
from SQL_Handler import DBHandler

db = DBHandler()
config = configparser.ConfigParser()


def send_mails(school_class: str, teacher_username: str):
    uuid_list = []
    with SMTP(config["email"]["server"]) as server:
        server.login(config["email"]["address"], config["email"]["password"])
        for email in db.Classes_Emails.get_class_emails(school_class):
            id = uuid.uuid4()
            #send mail via smtp
            msg = EmailHandler.build_email(email, teacher_username)
            server.sendmail(config["email"]["address"], msg['To'], msg.as_string())  # sent from, send to, email text
            uuid_list.append(str(id))
    return uuid_list


class EmailHandler:
    def __init__(self) -> None:
        #self.user config["email"]["address"]
        #self.password config["email"]["password"]
        #self.server config["email"]["server"]
        return

    def build_email(send_to: str, uuid: str, teacher_username: str):
        teacher_no_dot = teacher_username.replace(".", " ")

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
        return msg




if __name__ == "__main__":      # for testing on pc
    input("Start Test: Press Enter")
    config.read("../../config.ini")
    student_email_content_path = "templates/student_email_content.html"

