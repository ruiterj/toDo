from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/', views.tasks_view, name='tasks'),
    path('overview/', views.overview, name='overview'),
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('tasks/edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('tasks/push_status/<int:task_id>/', views.push_status, name='push_status'),
    path('update-day-plan-order/', views.update_day_plan_order, name='update_day_plan_order'),
    path('finish-task/<int:task_id>/', views.finish_task, name='finish_task'),
    path('tasks/move_to_in_progress/<int:task_id>/', views.move_to_in_progress, name='move_to_in_progress'),
]