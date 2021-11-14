from django.conf.urls import url 
from questions import views 

urlpatterns = [ 
    url(r'^api/questions$', views.question_base_handler),
    url(r'^api/questions/(?P<id>[0-9]+)$', views.question_detail_handler),
    url(r'^api/questions/checker/grammar$', views.question_grammar_check_handler),
    url(r'^api/questions/checker/similiar$', views.similiar_question_check_handler)
]
