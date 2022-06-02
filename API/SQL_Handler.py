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

    def write_class_mails(self, school_class : str, mail_list : list):
        for mail in mail_list:
            #sql INSERT INTO `Classes_Emails` (Email_ID, School_Class, Email) VALUES (NULL, school_class, mail)
            pass
        return
    
    def get_class_mails(self, school_class : str) -> List:
        mail_list = []
        #sql Select Email FROM Classes_Emails WHERE School_Class = "4CHEL"
        for out in self.cur:
            mail_list.append(str(out[0]))
        return mail_list

    def write_UUID(self, teacher_id : int, school_class : str, answer_1 : int, answer_2 : int, answer_3 : int, answer_4 : int, uuid_used = False):
        #sql INSERT INTO `UUIDs`(UUID, Teacher_ID, School_Class, UUID_Used, `Answer_1`, `Answer_2`, `Answer_3`, `Answer_4`) VALUES ([value-1],[value-2],[value-3],[value-4],[value-5],[value-6],[value-7],[value-8])
        pass

    #Teachers_Classes
    def write_teacher_class_assignment(self, teacher_id : int, school_class : str):
        #sql INSERT INTO `Teachers_Classes` (Assignment_ID, Teacher_ID, School_Class) VALUES (NULL, teacher_id, school_class)
        pass

    def get_class_assignments(self, teacher_id : int ) -> List:
        #sql Select School_Class FROM Teachers_Classes WHERE Teacher_ID = teacher_id
        class_list = []
        for out in self.cur:
            class_list.append(str(out[0]))
        return class_list
