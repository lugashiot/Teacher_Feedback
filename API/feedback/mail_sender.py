import os, uuid, sys
from datetime import datetime
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configparser
sys.path.append("/home/pi/Feedback/API")
from SQL_Handler import DBHandler


config = configparser.ConfigParser()
config.read("config.ini")
student_email_content_path = "API/feedback/templates/student_email_content.html"


class Mail_Sender:
    def __init__(self) -> None:
        self.db = DBHandler()

    def __assignments_to_classes(self, assignment_ids: list[int]) -> list[str]:
        school_classes = []
        for assignment_id in assignment_ids:
            if assignment_id == 0:
                continue
            school_classes.append(self.db.Teachers_Assignments.get_assignment_by_id(assignment_id)[2])
        return school_classes
    
    def __send_emails_by_school_class(self, school_class: str, teacher_username: str) -> list[str]:
        uuid_list = []
        with SMTP(config["email"]["server"]) as server:
            server.login(config["email"]["address"], config["email"]["password"])
            for email in self.db.Classes_Emails.get_class_emails(school_class):
                id = str(uuid.uuid4())
                msg = EmailHandler.build_email(email, id, teacher_username)
                # TODO Try except with specific error if email doesnt exist !?
                server.sendmail(config["email"]["address"], msg['To'], msg.as_string())  # sent from, send to, email text
                uuid_list.append(id)
        return uuid_list

    def send_emails(self, poll_id: int, teacher_username: str):
        """
        Sends Emails to all Classes linked to given Poll in the Database\n
        Teacher/User needs to be verified before calling this method!
        """
        poll_assignments = self.db.Polls.get_poll_by_id(poll_id)[3] # List of Assignment_IDs
        poll_classes = self.__assignments_to_classes(poll_assignments)
        for school_class in poll_classes:
            uuid_list = self.__send_emails_by_school_class(school_class, teacher_username)
            self.db.UUIDs.write_uuids(uuid_list, poll_id, int(datetime.now().timestamp()))
        return True

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


if __name__ == "__main__":      
    # for testing on pc
    sys.path.append(os.path.split(os.getcwd())[0])
    from SQL_Handler import DBHandler
    input("Start Test: Press Enter")
    config.read("../../config.ini")
    student_email_content_path = "templates/student_email_content.html"
    send_mails("4CHEL", "Klaus.Bichler")
    Mail_Sender.sen