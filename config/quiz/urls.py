from django.urls import path
from . import views

urlpatterns = [
    path('', views.exam_list, name='exam_list'),
    path('exam/<int:exam_id>/', views.exam_detail, name='exam_detail'),
    path('exam/create/', views.exam_create, name='exam_create'),
    path('exam/<int:exam_id>/question/add/', views.question_create, name='question_create'),
    path('exam/update/<int:exam_id>', views.exam_create, name='exam_create'),
    path('exam/delete/<int:exam_id>/', views.exam_delete, name='exam_delete'),
    #path('exam/<int:exam_id>/question/edit/<int:exam_id>', views.question_create, name='question_update'),
    #path('exam/<int:exam_id>/question/remove/<int:exam_id>', views.question_create, name='question_delete'),
]