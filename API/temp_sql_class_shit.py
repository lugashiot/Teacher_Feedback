class Answer:
    def __init__(self, uuid: str, answers: list, feedback_text: str):
        self.uuid = uuid
        self.answers = answers
        self.feedback_text = feedback_text


class Question:
    def __init__(self, teacher_id: int, question_id: int, question_text: str, question_answer_opts: list):
        self.teacher_id = teacher_id
        self.question_id = question_id
        self.question_text = question_text
        self.question_answer_opts = question_answer_opts


class Poll:
    def __init__(self, teacher_id: int, poll_id: int, poll_name: str, poll_assignments: list, poll_questions: list, poll_answers: list, poll_time: int):
        self.teacher_id = teacher_id
        self.poll_id = poll_id
        self.poll_name = poll_name
        self.poll_assignments = poll_assignments
        self.poll_questions = poll_questions
        self.poll_answers = poll_answers
        self.poll_time = poll_time


class Teacher:
    def __init__(self, teacher_id: int, teacher_username: str, polls: list, assignments: list):
        self.teacher_id = teacher_id
        self.teacher_username = teacher_username
        self.polls = polls
        self.assignments = assignments


if __name__ == "__main__":
    q_0 = Question(0, 0, "Gay?", ["ok", "ok", "ok", "ok", "ok"])

    test_answer_0 = Answer("abcd", [1, 2, 3, 4, 5, 1], "Senn Gay")
    test_answer_1 = Answer("dcba", [2, 3, 4, 5, 1, 2], "Senn HS")

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


