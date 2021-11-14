from questions.models import Question, Topics
from questions.serializers import QuestionSerializer

from ml.grammar_correctness_predict import grammar_correctness_predict
from ml.similiarity_predict import similiarity_predict


def get_questions_by_topics():
    res = {}
    questions = Question.objects.all()
    questions = QuestionSerializer(questions, many=True).data
    for topic in Topics:
        arr = []
        for q in questions:
            if q['topic'] == topic:
                arr.append(q)
        res[topic] = arr
    return res

def get_question_detail_by_id(id):
    try: 
        question = Question.objects.get(pk=id) 
    except Question.DoesNotExist: 
        question = None

    question = QuestionSerializer(question).data
    similiars = check_all_similiar(question["question_text"])
    question["similiars"] = similiars

    return question

def insert_question_by_text(question_text):
    topic = predict_topic(question_text)
    Question.create_instance(topic, question_text).save()

def check_grammar(question_text):
    return grammar_correctness_predict(question_text)

def check_all_similiar(question_text):
    questions = Question.objects.all()
    questions = QuestionSerializer(questions, many=True).data

    similiar_question = []
    for q in questions:
        if similiarity_predict(question_text, q["question_text"]):
            similiar_question.append(q)

    return similiar_question

def predict_topic(question_text):
    return Topics[0]
