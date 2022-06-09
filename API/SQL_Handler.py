import mariadb
import sys


class DBHandler:
    def __init__(self) -> None:
        try:
            self.conn = mariadb.connect(
                user="feedback",
                password="susadmin1234",
                host="localhost",
                port=3306,
                database="School"
            )
            self.conn.auto_reconnect = True
            self.conn.autocommit = True
            self.cur = self.conn.cursor()
        
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)


# Classes_Emails
    def write_class_mails(self, school_class : str, mail_list : list):
        for mail in mail_list:
            #sql INSERT INTO `Classes_Emails` (Email_ID, School_Class, Email) VALUES (NULL, school_class, mail)
            self.cur.execute("INSERT INTO `Classes_Emails` (School_Class, Email) VALUES (?, ?);", (school_class, mail))
        return "write_class_mails done"
    
    def get_class_mails(self, school_class : str) -> list:
        mail_list = []
        #sql Select Email FROM Classes_Emails WHERE School_Class = 'school_class'
        self.cur.execute("Select Email FROM `Classes_Emails` WHERE School_Class = ?;", (school_class, ))
        for out in self.cur:
            mail_list.append(str(out[0]))
        return mail_list


# UUIDs
    def write_uuids(self, uuid_list : list, teacher_id : int, school_class : str, time : int):
        #sql INSERT INTO `UUIDs`(UUID, Teacher_ID, School_Class, UUID_Used) VALUES (uuid, teacher_id, school_class, uuid_used)
        for uuid in uuid_list:
            self.cur.execute("INSERT INTO `UUIDs` (UUID, Teacher_ID, School_Class, Sent_Time) VALUES (?, ?, ?, ?)", (uuid, teacher_id, school_class, time))
        return "write_uuid done"

    def write_answers(self, uuid : str, answer_1 : str, answer_2 : str, answer_3 : str, answer_4 : str, time : int):
        #sql UPDATE `UUIDs` SET (UUID_Used = True, `Answer_1` = answer_1, `Answer_2` = answer_2, `Answer_3` = answer_3, `Answer_4` = answer_4)
        self.cur.execute("UPDATE `UUIDs` SET UUID_Used = 1, Answer_1 = ?, Answer_2 = ?, Answer_3 = ?, Answer_4 = ?, Answered_Time = ? WHERE UUID = ?", (answer_1, answer_2, answer_3, answer_4, time, uuid))
        return "write_answers done"
    
    def is_uuid_used(self, uuid : str) -> bool:
        #sql SELECT UUID_Used FROM `UUIDs` WHERE UUID = uuid
        self.cur.execute("SELECT UUID_Used FROM `UUIDs` WHERE UUID = ?;", (uuid, ))
        for out in self.cur:
            if out[0] == 1:
                return True
            return False

    def get_answers_by_uuid(self, uuid : str) -> list:
        #sql SELECT Answer_1,Answer_2,Answer_3,Answer_4 FROM `UUIDs` WHERE UUID = uuid
        self.cur.execute("SELECT Answer_1,Answer_2,Answer_3,Answer_4 FROM `UUIDs` WHERE UUID = ?;", (uuid, ))
        answer_list = []
        for out in self.cur:
            for answer in out:
                answer_list.append(int(answer))
            # if an unvalid/unfilled answer is in the answerset, give back an empty one
            if 0 in answer_list:
                return []
            return answer_list

    def get_answers_for_class(self, teacher_id : int, school_class : str):
        #sql Select Answer_1,Answer_2,Answer_3,Answer_4 FROM `UUIDs` WHERE (Teacher_ID = teacher_id AND School_Class = school_class)
        self.cur.execute("SELECT Answer_1,Answer_2,Answer_3,Answer_4 FROM `UUIDs` WHERE (Teacher_ID = ? AND School_Class = ?);", (teacher_id, school_class))
        answer_list_list = []
        # iterate through every answerset given
        for out in self.cur:
            answer_list = []
            # iterate through every answer of the current answerset
            for answer in out:
                answer_list.append(int(answer))
            # if any answer in the answerset is 0, dont use it
            if 0 in answer_list:
                continue
            answer_list_list.append(answer_list)
        return answer_list_list

    def get_all_uuids(self):
        #sql Select UUID FROM `UUIDs`
        self.cur.execute("SELECT UUID FROM `UUIDs`")
        uuid_list = []
        for out in self.cur:
            uuid_list.append(str(out[0]))
        return uuid_list

    def get_teacher_id_by_uuid(self, uuid):
        #sql Select Teacher_ID FROM `UUIDs` WHERE UUID = uuid
        self.cur.execute("SELECT Teacher_ID FROM `UUIDs` WHERE UUID = ?", (uuid, ))
        for out in self.cur:
            return out[0]

    def get_school_class_by_uuid(self, uuid):
        #sql Select Teacher_ID FROM `UUIDs` WHERE UUID = uuid
        self.cur.execute("SELECT School_Class FROM `UUIDs` WHERE UUID = ?", (uuid, ))
        for out in self.cur:
            return out[0]


# Teachers_Classes
    def write_teacher_class_assignment(self, teacher_id : int, school_class : str, subject : str):
        #sql INSERT INTO `Teachers_Classes` (Assignment_ID, Teacher_ID, School_Class, Subject) VALUES (NULL, teacher_id, school_class, Subject)
        self.cur.execute("INSERT INTO `Teachers_Classes` (Assignment_ID, Teacher_ID, School_Class, Subject) VALUES (NULL, ?, ?, ?);", (teacher_id, school_class, subject))
        return "write_teacher_class_assignment done"

    def add_questions_to_assignment(self, teacher_id : str, school_class : str, subject : str, question_id_1 : int, question_id_2 : int, question_id_3 : int, question_id_4 : int, assignment_id = 0):
        if assignment_id == 0:
            assignment_id = self.get_assignment_id(teacher_id, school_class, subject)
        #sql Update `Teachers_Classes` SET Question_1 = question_id_1, Question_2 = question_id_2, Question_3 = question_id_3, Question_4 = question_id_4 WHERE Assignment_ID = assignment_id
        self.cur.execute("Update `Teachers_Classes` SET Question_1 = ?, Question_2 = ?, Question_3 = ?, Question_4 = ? WHERE Assignment_ID = ?", (question_id_1, question_id_2, question_id_3, question_id_4, assignment_id))
        return "add_questions_to_assignment done"
        
    def get_class_assignments(self, teacher_id : int) -> list:
        #sql Select School_Class FROM `Teachers_Classes` WHERE Teacher_ID = teacher_id
        self.cur.execute("Select School_Class,Subject FROM `Teachers_Classes` WHERE Teacher_ID = ?;", (teacher_id, ))
        class_list = []
        for out in self.cur:
            class_list.append(str(out[0]) + " - " + str(out[1]))
        return class_list

    def get_assignment_id(self, teacher_id : str, school_class : str, subject : str) -> int:
        #sql Select Assignment_ID FROM `Teachers_Classes` WHERE Teacher_ID = teacher_id AND School_Class = school_class AND Subject = subject
        self.cur.execute("Select Assignment_ID FROM `Teachers_Classes` WHERE Teacher_ID = ? AND School_Class = ? AND Subject = ?", (teacher_id, school_class, subject))
        for out in self.cur:
            return int(out[0])
    
    def get_question_ids(self, teacher_id : str, school_class : str, subject : str, assignment_id = 0) -> list: #assignment_id OVERRIDES other parameters
        if assignment_id == 0:
            assignment_id = self.get_assignment_id(teacher_id, school_class, subject)
        #sql Select Question_1,Question_2,Question_3,Question_4 FROM `Teachers_Classes` WHERE Assignment_ID = assignment_id
        self.cur.execute("Select Question_1,Question_2,Question_3,Question_4 FROM `Teachers_Classes` WHERE Assignment_ID = ?;", (assignment_id, ))
        question_list = []
        for out in self.cur:
            for elem in out:
                question_list.append(elem)
            return question_list


# Teachers
    def write_teacher(self, username : str, forename : str, lastname : str, email : str):
        #sql INSERT INTO `Teachers` (Teacher_ID, Username, Forename, Lastname, Email) VALUES (NULL, username, forename, lastname, email)
        self.cur.execute("INSERT INTO `Teachers` (Teacher_ID, Username, Forename, Lastname, Email) VALUES (NULL, ?, ?, ?, ?);", (username, forename, lastname, email))
        return "write_teacher done"

    def get_teacher_by_id(self, teacher_id, wanted_key = ""):
        #sql Select * FROM `Teachers` WHERE Teacher_ID = teacher_id
        self.cur.execute("Select * FROM `Teachers` WHERE Teacher_ID = ?;", (teacher_id, ))
        for out in self.cur:
            return self.teacher_formatter(out, wanted_key)

    def get_teacher_by_username(self, username, wanted_key = ""):
        #sql Select * FROM `Teachers` WHERE Username = username      
        self.cur.execute("Select * FROM `Teachers` WHERE Username = ?;", (username, ))
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


# Questions
    def write_question(self, teacher_id : int, question_text : str, ans_opt_1 : str, ans_opt_2 : str, ans_opt_3 : str, ans_opt_4 : str, ans_opt_5 : str, is_public = 0):
        #sql INSERT INTO `Questions` (Question_ID, Teacher_ID, Is_Public, Question_Text, Answer_Option_1, Answer_Option_2, Answer_Option_3, Answer_Option_4, Answer_Option_5) VALUES (NULL, teacher_id, is_public, question_text, ans_opt_1, ans_opt_2, ans_opt_3, ans_opt_4, ans_opt_5)
        self.cur.execute("INSERT INTO `Questions` (Question_ID, Teacher_ID, Is_Public, Question_Text, Answer_Option_1, Answer_Option_2, Answer_Option_3, Answer_Option_4, Answer_Option_5) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)", (teacher_id, is_public, question_text, ans_opt_1, ans_opt_2, ans_opt_3, ans_opt_4, ans_opt_5))
        return "write_question done"

# SQL HANDLER NOT READY TO USE

if __name__ == "__main__":
    db = DBHandler()
    print("handled")

    print(db.get_class_mails("4CHEL"))
    x = db.get_teacher_by_id(8)
    print(x)
    print(x["Forename"])
    print(db.get_teacher_by_username("Christian.Hilpold", "Email"))
    print(db.get_class_assignments(8))
    #print(Handle.get_answers_for_class(1, "4CHEL"))
    #print(Handle.is_UUID_Used("aeeeaa69420-42069ae"))