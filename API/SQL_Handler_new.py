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
                database="Teacher_Feedback"
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
                database="Teacher_Feedback"
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
                database="Teacher_Feedback"
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
                database="Teacher_Feedback"
            )
            self.conn.auto_reconnect = True
            self.conn.autocommit = True
            self.cur = self.conn.cursor()
        
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)    

    def write_class_mail(self, school_class : str, email : str):
        #sql INSERT INTO `Classes_Emails` (Email_ID, School_Class, Email) VALUES (NULL, school_class, email)
        self.cur.execute("INSERT INTO `Classes_Emails` (Email_ID, School_Class, Email) VALUES (NULL, ?, ?)", (school_class, email))
        return "Classes_Emails.write_class_mail done"

    def write_class_mails(self, school_class : str, email_list : list):
        for email in email_list:
            #sql INSERT INTO `Classes_Emails` (Email_ID, School_Class, Email) VALUES (NULL, school_class, email)
            self.cur.execute("INSERT INTO `Classes_Emails` (School_Class, Email) VALUES (?, ?);", (school_class, email))
        return "write_class_mails done"
    
    def get_class_mails(self, school_class : str) -> list:
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
                database="Teacher_Feedback"
            )
            self.conn.auto_reconnect = True
            self.conn.autocommit = True
            self.cur = self.conn.cursor()
        
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)


# UUIDs
class UUIDs():
    def __init__(self) -> None:
        try:
            self.conn = mariadb.connect(
                user="feedback",
                password="susadmin1234",
                host="localhost",
                port=3306,
                database="Teacher_Feedback"
            )
            self.conn.auto_reconnect = True
            self.conn.autocommit = True
            self.cur = self.conn.cursor()
        
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)    

    def write_UUID(self, uuid : str, poll_id : int, sent_time : int):
        #sql INSERT INTO `UUIDs`(UUID, Poll_ID, Sent_Time) VALUES (uuid, poll_id, sent_time)
        self.cur.execute("INSERT INTO `UUIDs`(UUID, Poll_ID, Sent_Time) VALUES (?, ?, ?)", (uuid, poll_id, sent_time))
        return

    


# Questions
class Questions():
    def __init__(self) -> None:
        try:
            self.conn = mariadb.connect(
                user="feedback",
                password="susadmin1234",
                host="localhost",
                port=3306,
                database="Teacher_Feedback"
            )
            self.conn.auto_reconnect = True
            self.conn.autocommit = True
            self.cur = self.conn.cursor()
        
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)



if __name__ == "__main__":
    db = DBHandler()
    print("handled")
    db.Teachers.write_teacher()
    
    print(db.get_class_mails("4CHEL"))
    x = db.get_teacher_by_id(8)
    print(x)
    print(x["Forename"])
    print(db.get_teacher_by_username("Christian.Hilpold", "Email"))
    print(db.get_class_assignments(8))
    #print(Handle.get_answers_for_class(1, "4CHEL"))
    #print(Handle.is_UUID_Used("aeeeaa69420-42069ae"))