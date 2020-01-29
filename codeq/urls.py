from django.urls import path

from codeq import views

app_name = 'codeq'

urlpatterns = [
    # quetions
    path('', views.QuestionList.as_view(), name='question_list'),
    path('question/new/', views.UploadQuestion.as_view(), name='create_question'),
    path('question/<str:slug>/', views.QuestionDetail.as_view(), name='question_detail'),
    path('question/delete/<str:slug>/', views.DeleteQuestion.as_view(), name='delete_question'),

    # answer
    path('question/answer/<str:slug>/', views.add_answer, name='add_answer'),
    path('question/answer/delete/<str:slug>/', views.delete_answer, name='delete_answer'),

    # reply
    path('question/answer/reply/<str:slug>/', views.add_reply, name='add_reply'),
    path('question/answer/reply/delete/<int:pk>/', views.delete_reply, name='delete_reply'),
]
