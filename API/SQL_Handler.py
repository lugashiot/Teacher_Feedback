from typing import Optional
import mariadb
import sys

# TODO 
# Look for str lengths bc of sql bullshit


class DBHandler:
    def __init__(self) -> None:
        self.Teachers = Teachers()
        self.Teachers_Assignments = Teachers_Assignments()
        self.Classes_Emails = Classes_Emails()
        self.Polls = Polls()
        self.UUIDs = UUIDs()
        self.Questions = Questions()
        """ # in every init to create a connection
        try:
            self.conn = mariadb.connect(
                user="feedback",
                password="susadmin1234",
                host="localhost",
                port=3306,
                database="Feedback"
            )
            #self.conn.auto_reconnect = True
            #self.conn.autocommit = True
            #self.cur = self.conn.cursor()
            
        
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        """


# Teachers
class Teachers():
    def __init__(self) -> None:
        try:
            self.conn = mariadb.connect(
                user="feedback",
                password="susadmin1234",
                host="localhost",
                port=3306,
                database="Feedback"
            )
            self.conn.auto_reconnect = True
            self.conn.autocommit = True
            self.cur = self.conn.cursor()
        
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

    def write_teacher(self, username : str, forename : str, lastname : str, email : str):
        #sql INSERT INTO `Teachers` (Teacher_ID, Username, Forename, Lastname, Email) VALUES (NULL, username, forename, lastname, email)
        self.cur.execute("INSERT INTO `Teachers` (Teacher_ID, Username, Forename, Lastname, Email) VALUES (NULL, ?, ?, ?, ?);", (username, forename, lastname, email))
        return "write_teacher done"

    def get_teacher_by_id(self, teacher_id, wanted_key = ""):
        #sql Select * FROM `Teachers` WHERE Teacher_ID = teacher_id     alle aber in genau der Reihenfolge
        self.cur.execute("Select Teacher_ID,Username,Forename,Lastname,Email FROM `Teachers` WHERE Teacher_ID = ?;", (teacher_id, ))
        for out in self.cur:
            return self.teacher_formatter(out, wanted_key)

    def get_teacher_by_username(self, username, wanted_key = ""):
        #sql Select * FROM `Teachers` WHERE Username = username         alle aber in genau der Reihenfolge 
        self.cur.execute("Select Teacher_ID,Username,Forename,Lastname,Email FROM `Teachers` WHERE Username = ?;", (username, ))
        for out in self.cur:
            return self.teacher_formatter(out, wanted_key)

    def get_all_teachers_username(self):
        #sql Select Username FROM `Teachers`
        self.cur.execute("Select Username FROM `Teachers`")
        teacher_list = []
        for out in self.cur:
            teacher_list.append(str(out[0]))
        return teacher_list
    
    def teacher_formatter(self, out, wanted_key):
        teacher = {
            "Teacher_ID" : out[0],
            "Username" : out[1],
            "Forename" : out[2],
            "Lastname" : out[3],
            "Email" : out[4]
        }

        for key in teacher.keys():
            if key == wanted_key:
                return teacher[key]
        return teacher


# Teachers_Assignments
class Teachers_Assignments():
    def __init__(self) -> None:
        try:
            self.conn = mariadb.connect(
                user="feedback",
                password="susadmin1234",
                host="localhost",
                port=3306,
                database="Feedback"
            )
            self.conn.auto_reconnect = True
            self.conn.autocommit = True
            self.cur = self.conn.cursor()
        
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)    

    def write_assignment(self, teacher_id : int, school_class : str):
        #sql INSERT INTO `Teachers_Assignments` (Assignment_ID, Teacher_ID, School_Class) VALUES (NULL, teacher_id, school_class)
        self.cur.execute("INSERT INTO `Teachers_Assignments` (Assignment_ID, Teacher_ID, School_Class) VALUES (NULL, ?, ?);", (teacher_id, school_class))
        return "Teachers_Assignments.write_assignment done"

    def get_assignments_from_teacher(self, teacher_id : int) -> list:
        #sql Select School_Class FROM `Teachers_Assignments` WHERE Teacher_ID = teacher_id
        self.cur.execute("Select School_Class FROM `Teachers_Assignments` WHERE Teacher_ID = ?;", (teacher_id, ))
        assignment_list = []
        for out in self.cur:
            assignment_list.append(str(out[0]))   # example: ["4CHEL", "3CHEL"]
        return assignment_list
    
    def get_assignment_id(self, teacher_id : int, school_class : str) -> int:
        #sql Select Assignment_ID FROM `Teachers_Assignments` WHERE Teacher_ID = teacher_id AND School_Class = school_class
        self.cur.execute("Select Assignment_ID FROM `Teachers_Assignments` WHERE Teacher_ID = ? AND School_Class = ?", (teacher_id, school_class))
        for out in self.cur:
            return int(out[0])

    def get_assignment_by_id(self, assignment_id : int) -> list:
        #sql Select Assignment_ID,Teacher_ID,School_Class,Subject FROM `Teachers_Assignments` WHERE Assignment_ID = assignment_id
        self.cur.execute("Select Assignment_ID,Teacher_ID,School_Class FROM `Teachers_Assignments` WHERE Assignment_ID = ?", (assignment_id, ))
        for out in self.cur:
            return list(out)


# Classes_Emails
class Classes_Emails():
    def __init__(self) -> None:
        try:
            self.conn = mariadb.connect(
                user="feedback",
                password="susadmin1234",
                host="localhost",
                port=3306,
                database="Feedback"
            )
            self.conn.auto_reconnect = True
            self.conn.autocommit = True
            self.cur = self.conn.cursor()
        
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)    

    def write_class_email(self, school_class : str, email : str):
        #sql INSERT INTO `Classes_Emails` (Email_ID, School_Class, Email) VALUES (NULL, school_class, email)
        self.cur.execute("INSERT INTO `Classes_Emails` (Email_ID, School_Class, Email) VALUES (NULL, ?, ?)", (school_class, email))
        return "Classes_Emails.write_class_mail done"

    def write_class_emails(self, school_class : str, email_list : list):
        for email in email_list:
            #sql INSERT INTO `Classes_Emails` (Email_ID, School_Class, Email) VALUES (NULL, school_class, email)
            self.cur.execute("INSERT INTO `Classes_Emails` (School_Class, Email) VALUES (?, ?);", (school_class, email))
        return "write_class_mails done"
    
    def get_class_emails(self, school_class : str) -> list:
        #sql Select Email FROM `Classes_Emails` WHERE School_Class = school_class
        self.cur.execute("Select Email FROM `Classes_Emails` WHERE School_Class = ?", (school_class, ))
        email_list = []
        for out in self.cur:
            email_list.append(str(out[0]))
        return email_list


# Polls
class Polls():
    def __init__(self) -> None:
        try:
            self.conn = mariadb.connect(
                user="feedback",
                password="susadmin1234",
                host="localhost",
                port=3306,
                database="Feedback"
            )
            self.conn.auto_reconnect = True
            self.conn.autocommit = True
            self.cur = self.conn.cursor()
        
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
    
    def write_poll(self, teacher_id : int, poll_name : str, assigment_id_1 : int, assigment_id_2 : int, assigment_id_3 : int, assigment_id_4 : int, assigment_id_5 : int, question_id_1 : int, question_id_2 : int, question_id_3 : int, question_id_4 : int, question_id_5 : int, question_id_6 : int, poll_time : int):
        #sql INSERT INTO `Polls` (Teacher_ID, Poll_Name, Ass_1, Ass_2, Ass_3, Ass_4, Ass_5, Q_ID_1, Q_ID_2, Q_ID_3, Q_ID_4, Q_ID_5, Q_ID_6, Poll_Time) VALUES ()
        self.cur.execute("INSERT INTO `Polls` (Teacher_ID, Poll_Name, Ass_1, Ass_2, Ass_3, Ass_4, Ass_5, Q_ID_1, Q_ID_2, Q_ID_3, Q_ID_4, Q_ID_5, Q_ID_6, Poll_Time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (teacher_id, poll_name, assigment_id_1, assigment_id_2, assigment_id_3, assigment_id_4, assigment_id_5, question_id_1, question_id_2, question_id_3, question_id_4, question_id_5, question_id_6, poll_time))
        return "Polls.write_poll done"

    def get_polls_by_teacher(self, teacher_id : int):
        #sql Select Poll_ID,Teacher_ID,Poll_Name,Ass_1,Ass_2,Ass_3,Ass_4,Ass_5,Q_ID_1,Q_ID_2,Q_ID_3,Q_ID_4,Q_ID_5,Q_ID_6,Poll_Time FROM `Polls` WHERE Teacher_ID = teacher_id
        self.cur.execute("Select Poll_ID,Teacher_ID,Poll_Name,Ass_1,Ass_2,Ass_3,Ass_4,Ass_5,Q_ID_1,Q_ID_2,Q_ID_3,Q_ID_4,Q_ID_5,Q_ID_6,Poll_Time FROM `Polls` WHERE Teacher_ID = ?", (teacher_id, ))
        poll_list = []
        for out in self.cur:
            poll_list.append([int(out[0]), int(out[1]), str(out[2]), [int(out[3]), int(out[4]), int(out[5]), int(out[6]), int(out[7])], [int(out[8]), int(out[9]), int(out[10]), int(out[11]), int(out[12]), int(out[13])], int(out[14].timestamp())])
        return poll_list 

    def get_poll_by_id(self, poll_id: int):
        #sql Select Poll_ID,Teacher_ID,Poll_Name,Ass_1,Ass_2,Ass_3,Ass_4,Ass_5,Q_ID_1,Q_ID_2,Q_ID_3,Q_ID_4,Q_ID_5,Q_ID_6,Poll_Time FROM `Polls` WHERE Poll_ID = poll_id
        self.cur.execute("Select Poll_ID,Teacher_ID,Poll_Name,Ass_1,Ass_2,Ass_3,Ass_4,Ass_5,Q_ID_1,Q_ID_2,Q_ID_3,Q_ID_4,Q_ID_5,Q_ID_6,Poll_Time FROM `Polls` WHERE Poll_ID = ?", (poll_id, ))
        for out in self.cur:
            # [Poll_ID, Teacher_ID, Poll_Name, List[Assignment_IDs], List[Question_IDs], Poll_Time]
            return [int(out[0]), int(out[1]), str(out[2]), [int(out[3]), int(out[4]), int(out[5]), int(out[6]), int(out[7])], [int(out[8]), int(out[9]), int(out[10]), int(out[11]), int(out[12]), int(out[13])], int(out[14].timestamp())]
    
    def get_questions_by_id(self, poll_id : int):
        #sql Select Q_ID_1,Q_ID_2,Q_ID_3,Q_ID_4,Q_ID_5,Q_ID_6 FROM `Polls` WHERE Poll_ID = poll_id
        self.cur.execute("Select Q_ID_1,Q_ID_2,Q_ID_3,Q_ID_4,Q_ID_5,Q_ID_6 FROM `Polls` WHERE Poll_ID = ?", (poll_id, ))
        question_ids = []
        for out in self.cur:
            for qid in out:
                question_ids.append(int(qid))
            return question_ids


# UUIDs
class UUIDs():
    def __init__(self) -> None:
        try:
            self.conn = mariadb.connect(
                user="feedback",
                password="susadmin1234",
                host="localhost",
                port=3306,
                database="Feedback"
            )
            self.conn.auto_reconnect = True
            self.conn.autocommit = True
            self.cur = self.conn.cursor()
        
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)    

    def write_uuid(self, uuid : str, poll_id : int):   # Dont use this one in mail_sender
        #sql INSERT INTO `UUIDs`(UUID, Poll_ID) VALUES (uuid, poll_id)
        self.cur.execute("INSERT INTO `UUIDs`(UUID, Poll_ID) VALUES (?, ?)", (uuid, poll_id))
        return "UUIDs.write_UUID done"

    def write_uuids(self, uuid_list : list, poll_id : int):
        for uuid in uuid_list:
            #sql INSERT INTO `UUIDs`(UUID, Poll_ID) VALUES (uuid, poll_id)
            self.cur.execute("INSERT INTO `UUIDs`(UUID, Poll_ID) VALUES (?, ?)", (uuid, poll_id))
        return "UUIDs.write_UUIDs done"
    
    def write_answers(self, uuid : str, answer_1 : int, answer_2 : int, answer_3 : int, answer_4 : int, answer_5 : Optional[int], answer_6 : Optional[int], answer_textfield : Optional[str], answered_time : int):
        #sql UPDATE `UUIDs` SET (UUID_Used = True, Answer_1 = answer_1, Answer_2 = answer_2, Answer_3 = answer_3, Answer_4 = answer_4, Answer_5 = answer_5, Answer_6 = Answer_6, Answer_Textfield = answer_text_field, Answered_Time = answered_time)
        self.cur.execute("UPDATE `UUIDs` SET (UUID_Used = 1, Answer_1 = ?, Answer_2 = ?, Answer_3 = ?, Answer_4 = ?, Answer_5 = ?, Answer_6 = ?, Answer_Textfield = ?, Answered_Time = ?) WHERE UUID = ?", (answer_1, answer_2, answer_3, answer_4, answer_5, answer_6, answer_textfield, answered_time, uuid))
        return "UUIDs.write_Answers done"
    
    def get_answer_by_uuid(self, uuid):
        #sql Select Answer_1,Answer_2,Answer_3,Answer_4,Answer_5,Answer_6,Answer_Textfield FROM `UUIDs` WHERE UUID = uuid
        self.cur.execute("Select Answer_1,Answer_2,Answer_3,Answer_4,Answer_5,Answer_6,Answer_Textfield FROM `UUIDs` WHERE UUID = ?", (uuid, ))
        for out in self.cur:
            return [int(out[0]), int(out[1]), int(out[2]), int(out[3]), int(out[4]), int(out[5]), str(out[6])] # 6th is textfield

    def get_answers_by_poll_id(self, poll_id : int):
        #sql Select 
        self.cur.execute("Select Answer_1,Answer_2,Answer_3,Answer_4,Answer_5,Answer_6,Answer_Textfield FROM `UUIDs` WHERE Poll_ID = ?", (poll_id, ))
        answer_list = []
        for out in self.cur:
            answer_list.append([int(out[0]), int(out[1]), int(out[2]), int(out[3]), int(out[4]), int(out[5]), str(out[6])]) # 6th is textfield
        return answer_list

    def get_uuids_by_poll_id(self, poll_id : int):
        #sql Select UUID FROM `UUIDs` WHERE Poll_ID = poll_id
        self.cur.execute("Select UUID FROM `UUIDs` WHERE Poll_ID = ?", (poll_id, ))
        uuid_list = []
        for out in self.cur:
            uuid_list.append(str(out[0]))
        return uuid_list

    def get_all_uuids(self) -> list[str]:
        uuid_list = []
        #sql Select UUID FROM `UUIDs` WHERE 1
        self.cur.execute("Select UUID FROM `UUIDs` WHERE 1")
        for out in self.cur:
            uuid_list.append(str(out[0]))
        return uuid_list

    def is_used(self, uuid : str):
        #sql Select UUID_Used FROM `UUIDs` WHERE UUID = uuid
        self.cur.execute("Select UUID_Used FROM `UUIDs` WHERE UUID = ?", (uuid, ))
        for out in self.cur:    
            if out[0] == 1:
                return True
            return False
            

# Questions
class Questions():
    def __init__(self) -> None:
        try:
            self.conn = mariadb.connect(
                user="feedback",
                password="susadmin1234",
                host="localhost",
                port=3306,
                database="Feedback"
            )
            self.conn.auto_reconnect = True
            self.conn.autocommit = True
            self.cur = self.conn.cursor()
        
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

    def write_question(self, teacher_id : int, question_text : str, answer_options: list, question_public = 0):
        #sql INSERT INTO `Questions` (Teacher_ID, Question_Text, Ans_Opt_1, Ans_Opt_2, Ans_Opt_3, Ans_Opt_4, Ans_Opt_5, Question_Public) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        self.cur.execute("INSERT INTO `Questions` (Teacher_ID, Question_Text, Ans_Opt_1, Ans_Opt_2, Ans_Opt_3, Ans_Opt_4, Ans_Opt_5, Question_Public) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (teacher_id, question_text, answer_options[0], answer_options[1], answer_options[2], answer_options[3], answer_options[4], question_public))
        return "Questions.write_question done"
    
    def get_questions_by_teacher(self, teacher_id: int):
        #sql Select Question_ID,Question_Text,Ans_Opt_1,Ans_Opt_2,Ans_Opt_3,Ans_Opt_4,Ans_Opt_5 FROM `Questions` WHERE Teacher_ID = teacher_id
        self.cur.execute("Select Question_ID,Question_Text,Ans_Opt_1,Ans_Opt_2,Ans_Opt_3,Ans_Opt_4,Ans_Opt_5,Teacher_ID FROM `Questions` WHERE Teacher_ID = ?", (teacher_id, ))
        question_list = []
        for out in self.cur:
            question_list.append([int(out[0]), str(out[1]), [str(out[2]), str(out[3]), str(out[4]), str(out[5]), str(out[6])], int(out[7])])
        return question_list    
        # Question_ID, Question_Text, [Ans_Opts], Teacher_ID

    def get_question_by_id(self, question_id : int):
        #sql Select Question_ID,Question_Text,Ans_Opt_1,Ans_Opt_2,Ans_Opt_3,Ans_Opt_4,Ans_Opt_5,Teacher_ID FROM `Questions` WHERE Question_ID = question_id
        self.cur.execute("Select Question_ID,Question_Text,Ans_Opt_1,Ans_Opt_2,Ans_Opt_3,Ans_Opt_4,Ans_Opt_5,Teacher_ID FROM `Questions` WHERE Question_ID = ?", (question_id, ))
        for out in self.cur:
            return [int(out[0]), str(out[1]), [str(out[2]), str(out[3]), str(out[4]), str(out[5]), str(out[6])], int(out[7])]
            # Question_ID, Question_Text, [Ans_Opts], Teacher_ID
    
    def get_public_questions(self):
        #sql Select Question_ID,Question_Text,Ans_Opt_1,Ans_Opt_2,Ans_Opt_3,Ans_Opt_4,Ans_Opt_5,Teacher_ID FROM `Questions` WHERE Question_Public = 1
        self.cur.execute("Select Question_ID,Question_Text,Ans_Opt_1,Ans_Opt_2,Ans_Opt_3,Ans_Opt_4,Ans_Opt_5,Teacher_ID FROM `Questions` WHERE Question_Public = 1")
        question_list = []
        for out in self.cur:
            question_list.append([int(out[0]), str(out[1]), [str(out[2]), str(out[3]), str(out[4]), str(out[5]), str(out[6])], int(out[7])])
        return question_list    
        # Question_ID, Question_Text, [Ans_Opts], Teacher_ID


if __name__ == "__main__":
    db = DBHandler()
    print("handled")
    
    print(db.Teachers.get_all_teachers_username())
    print(db.Classes_Emails.get_class_emails("4CHEL"))
    #x = db.Teachers.get_teacher_by_id(8)
    #print(x)
    #print(x["Forename"])
    #print(db.Teachers.get_teacher_by_username("Christian.Hilpold", "Email"))
    #print(db.Teachers_Assignments.get_assignments_from_teacher(8))
    #print(db.UUIDs.get_answers_by_poll_id(17))
    #print(db.UUIDs.is_used("aeeeaa69420-42069ae"))