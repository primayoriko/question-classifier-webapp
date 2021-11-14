from questions.models import Question, Topics

def get_questions_by_topics():
    res = {}
    questions = Question.objects.all()
    for topic in Topics:
        arr = []
        for q in questions:
            if q.topic == topic:
                arr.append(q)
        res[topic] = arr
    return res

def insert_question(question):
    question.save()

def check_grammar(question):
    return True

def check_all_similiar(question):
    pass

def predict_topic(question):
    return Topics[0]

def get_question_by_id(id):
    try: 
        question = Question.objects.get(pk=id) 
    except Question.DoesNotExist: 
        question = None

    return question