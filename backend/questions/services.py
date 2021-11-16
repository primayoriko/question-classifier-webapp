from questions.models import Question, Topics
from questions.serializers import QuestionSerializer

from ml.grammar_correctness_predict import grammar_correctness_predict
from ml.similiarity_predict import similiarity_predict
from ml.topic_classification_predict import topic_classification_predict


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
        return None

    question = QuestionSerializer(question).data
    similiars = check_all_similiar(question["question_text"], question["topic"], id)
    question["similiars"] = similiars

    return question

def insert_question_by_text(question_text):
    isGrammarValid = check_grammar_by_text(question_text)
    topic = check_topic_by_text(question_text)
    isQuestionUnique = len(check_all_similiar(question_text, topic=topic))==0
    if (isGrammarValid and isQuestionUnique):
        Question.create_instance(topic, question_text).save()
        return True, None
    else:
        causes = []
        if (not isGrammarValid):
            causes.append("the grammar is invalid")
        if (not isQuestionUnique):
            causes.append("this question is not unique")
        return False, causes

def delete_question(id=None):
    if id is None:
        return Question.objects.filter().delete()
    else:
        return Question.objects.filter(pk=id).delete()

def check_grammar_by_text(question_text):
    return grammar_correctness_predict(question_text)

def check_all_similiar(question_text, topic=None, id=None):
    topic = topic if topic is not None else check_topic_by_text(question_text)
    questions = Question.objects.all()
    questions = QuestionSerializer(questions, many=True).data
    similiar_question = []

    for q in questions:
        if topic == q["topic"] and id != str(q["id"]) and similiarity_predict(question_text, q["question_text"]):
            similiar_question.append(q)

    return similiar_question

def check_topic_by_text(question_text):
    return topic_classification_predict(question_text)
