from typing import List
import mariadb, sys

class DBHandler():
    def __init__(self) -> None:
        try:
            conn = mariadb.connect(
                user="feedback",
                password="susadmin1234",
                host="localhost",
                port=3306,
                database="School"
            )
            conn.autocommit = True
            self.cur = conn.cursor()
        
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)


# Classes_Emails
    def write_class_mails(self, school_class : str, mail_list : list):
        for mail in mail_list:
            #sql INSERT INTO `Classes_Emails` (Email_ID, School_Class, Email) VALUES (NULL, school_class, mail)
            self.cur.execute("INSERT INTO `Classes_Emails` (Email_ID, School_Class, Email) VALUES (NULL, ?, ?);", (school_class, mail))
        return
    
    def get_class_mails(self, school_class : str) -> List:
        mail_list = []
        #sql Select Email FROM Classes_Emails WHERE School_Class = 'school_class'
        self.cur.execute("Select Email FROM `Classes_Emails` WHERE School_Class = '?';", (school_class))
        for out in self.cur:
            mail_list.append(str(out[0]))
        return mail_list


# UUIDs
    def write_UUID(self, uuid : str, teacher_id : int, school_class : str, uuid_used = False):
        #sql INSERT INTO `UUIDs`(UUID, Teacher_ID, School_Class, UUID_Used) VALUES (uuid, teacher_id, school_class, uuid_used)
        self.cur.execute("INSERT INTO `UUIDs` (UUID, Teacher_ID, School_Class, UUID_Used) VALUES (?, ?, ?, ?);", (uuid, teacher_id, school_class, uuid_used))
        return

    def write_Answers(self, uuid : str, answer_1 : int, answer_2 : int, answer_3 : int, answer_4 : int):
        #sql UPDATE `UUIDs` SET (UUID_Used = True, `Answer_1` = answer_1, `Answer_2` = answer_2, `Answer_3` = answer_3, `Answer_4` = answer_4)
        self.cur.execute("UPDATE `UUIDs` SET (UUID_Used = True, `Answer_1` = ?, `Answer_2` = ?, `Answer_3` = ?, `Answer_4` = ?) WHERE UUID = '?';", (answer_1, answer_2, answer_3, answer_4, uuid))
        return
    
    def is_UUID_Used(self, uuid : str):
        #sql SELECT UUID_Used FROM `UUIDs` WHERE UUID = uuid
        self.cur.execute("SELECT UUID_Used FROM `UUIDs` WHERE UUID = '?';", (uuid))
        for out in self.cur:
            return out[0]

    def get_Answers_by_uuid(self, uuid : str):
        #sql SELECT Answer_1,Answer_2,Answer_3,Answer_4 FROM `UUIDs` WHERE UUID = uuid
        self.cur.execute("SELECT Answer_1,Answer_2,Answer_3,Answer_4 FROM `UUIDs` WHERE UUID = '?';", (uuid))
        answer_list = []
        for out in self.cur:
            for answer in out:
                answer_list.append(int(answer))
            return answer_list

    def get_Answers_for_class(self, teacher_id : int, school_class : str):
        #sql Select Answer_1,Answer_2,Answer_3,Answer_4 FROM `UUIDs` WHERE (Teacher_ID = teacher_id AND School_Class = school_class)
        self.cur.execute("SELECT Answer_1,Answer_2,Answer_3,Answer_4 FROM `UUIDs` WHERE (Teacher_ID = ? AND School_Class = '?');", (teacher_id, school_class))
        answer_list_list = []
        for out in self.cur:
            answer_list = []
            for answer in out:
                answer_list.append(int(answer))
            answer_list_list.append(answer_list)
        return answer_list_list


# Teachers_Classes
    def write_teacher_class_assignment(self, teacher_id : int, school_class : str):
        #sql INSERT INTO `Teachers_Classes` (Assignment_ID, Teacher_ID, School_Class) VALUES (NULL, teacher_id, school_class)
        self.cur.execute("INSERT INTO `Teachers_Classes` (Assignment_ID, Teacher_ID, School_Class) VALUES (NULL, ?, ?);", (teacher_id, school_class))
        return

    def get_class_assignments(self, teacher_id : int ) -> List:
        #sql Select School_Class FROM Teachers_Classes WHERE Teacher_ID = teacher_id
        self.cur.execute("Select School_Class FROM `Teachers_Classes` WHERE Teacher_ID = '?';", (teacher_id))
        class_list = []
        for out in self.cur:
            class_list.append(str(out[0]))
        return class_list


# Teachers
    def write_teacher(self, username : str, forename : str, lastname : str, email : str):
        #sql INSERT INTO `Teachers` (Teacher_ID, Username, Forename, Lastname, Email) VALUES (NULL, username, forename, lastname, email)
        self.cur.execute("INSERT INTO `Teachers` (Teacher_ID, Username, Forename, Lastname, Email) VALUES (NULL, ?, ?, ?, ?);", (username, forename, lastname, email))
        return

    def get_teacher_by_id(self, teacher_id, wanted_key = ""):
        #sql Select * FROM `Teachers` WHERE Teacher_ID = teacher_id
        self.cur.execute("Select * FROM `Teachers` WHERE Teacher_ID = '?';", (teacher_id))
        for out in self.cur:
            self.teacher_formatter(wanted_key)
            return 

    def get_teacher_by_username(self, username, wanted_key = ""):
        #sql Select * FROM `Teachers` WHERE Username = username      
        self.cur.execute("Select * FROM `Teachers` WHERE Username = '?';", (username))
        for out in self.cur:
            return self.teacher_formatter(self.cur, wanted_key)
    
    def teacher_formatter(self, cursor, wanted_key):
        teacher = {}
        for out in cursor:
            teacher["Teacher_ID"] = out[0]
            teacher["Username"] = out[1]
            teacher["Forename"] = out[2]
            teacher["Lastname"] = out[3]
            teacher["Email"] = out[4]

        for key in teacher.keys():
            if key == wanted_key:
                return teacher[key]
        return teacher