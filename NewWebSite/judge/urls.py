from django.urls import path
from . import views

app_name = 'judge'

urlpatterns = [
    path('', views.problems_list, name='problems'),
    path('problem/<int:pk>/', views.problem_detail, name='problem_detail'),
    path('submissions/', views.my_submissions, name='my_submissions'),
]
