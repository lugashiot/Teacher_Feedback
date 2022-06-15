from dataclasses import dataclass, field
from SQL_Handler import DBHandler

db = DBHandler()


@dataclass
class Answer:
    uuid: str
    answers: list[int] = field(init=False)
    feedback_text: str = field(init=False)

    def __post_init__(self) -> None:
        answer_data = db.UUIDs.get_answer_by_uuid(self.uuid)
        self.answers = [i for i in answer_data if type(i) == int]
        self.feedback_text = answer_data[6]

@dataclass
class Question:
    question_id: int
    teacher_id: int = field(init=False)
    question_text: str = field(init=False)
    question_answer_opts: list[str] = field(init=False)
    
    def __post_init__(self) -> None:
        print(f"Question ID now: {self.question_id}")
        question_data = db.Questions.get_question_by_id(self.question_id)
        self.question_text = question_data[1]
        self.question_answer_opts = question_data[2]
        self.teacher_id = question_data[3]

@dataclass
class Poll:
    poll_id: int
    teacher_id: int = field(init=False)
    poll_name: str = field(init=False)
    poll_assignments: list[int] = field(init=False)
    poll_question_ids: list[int] = field(init=False)
    poll_questions: list[Question] = field(init=False)    # Question Instances
    poll_answers: list[Answer] = field(init=False)   # Student Answer Instances
    poll_time: int = field(init=False)
    poll_uuids: list[str] = field(init=False)

    def __post_init__(self) -> None:
        print(self.poll_id)
        poll_data = db.Polls.get_poll_by_id(self.poll_id)
        self.teacher_id = poll_data[1]
        self.poll_name = poll_data[2]
        self.poll_assignments = [i for i in poll_data[3] if i != 0]
        self.poll_question_ids = poll_data[4]
        self.poll_time = poll_data[5]
        self.poll_questions = [Question(i) for i in self.poll_question_ids if i != 0]
        self.poll_uuids = db.UUIDs.get_uuids_by_poll_id(self.poll_id)
        self.poll_answers = [Answer(i) for i in self.poll_uuids]


@dataclass
class Teacher:
    #def __init__(self, teacher_id: int, teacher_username: str, polls: list, assignments: list):
    teacher_username: str
    teacher_id: int = field(init=False)
    poll_ids: list[int] = field(init=False)
    polls: list[Poll] = field(init=False)
    assignments: list[str] = field(init=False)

    def __post_init__(self) -> None:
        self.teacher_id = db.Teachers.get_teacher_by_username(self.teacher_username, "Teacher_ID")
        poll_data = db.Polls.get_polls_by_teacher(self.teacher_id)
        self.poll_ids = [x[0] for x in poll_data]
        print("poll ids", self.poll_ids)
        self.polls = [Poll(i) for i in self.poll_ids]
        self.assignments = db.Teachers_Assignments.get_assignments_from_teacher(self.teacher_id)


if __name__ == "__main__":
    i = 1
    if i == 1:
        print(Question(2))
        
        print(Teacher("Klaus.Bichler"))
    
    else:
        q_0 = Question(0, 0, "Gay?", ["ok", "ok", "ok", "ok", "ok"])

        test_answer_0 = Answer([1, 2, 3, 4, 5, 1], "Senn Gay")
        test_answer_1 = Answer([2, 3, 4, 5, 1, 2], "Senn HS")

        test_poll_0 = Poll(0, 0, "Test1", ["4CHEL", "3CHEL"], [q_0, q_0, q_0, q_0, q_0, q_0], [test_answer_0, test_answer_1], 0000000)
        test_poll_1 = Poll(0, 1, "Test1", ["4CHEL", "3CHEL"], [q_0, q_0, q_0, q_0, q_0, q_0], [test_answer_0, test_answer_1], 0000000)

        teachers = [Teacher(0, "Gilbert.Senn", [test_poll_0, test_poll_1], ["4CHEL", "3CHEL"])]

        # get teacher by id
        for t in teachers:
            if t.teacher_id == 0:
                Senn = t

        # single values
        print(Senn.polls[0].poll_questions[0].question_text)
        print(Senn.polls[0].poll_questions[0].question_answer_opts)
        print()
        print(Senn.polls[0].poll_answers[0].answers)
        print(Senn.polls[0].poll_answers[0].feedback_text)
        print()

        # get all poll answers of Senn
        answers = [x.answers for x in Senn.polls[0].poll_answers]
        feedback_texts = [x.feedback_text for x in Senn.polls[0].poll_answers]
        print(answers)
        print(feedback_texts)
        print()

        # get all poll ids of Senn
        poll_ids = [x.poll_id for x in Senn.polls]
        print(poll_ids)
        print()
