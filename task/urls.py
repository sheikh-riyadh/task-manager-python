from django.urls import path
from task.views import employee_dashboard,manager_dashboard,create_task,show_tasks,update_task,delete_task

urlpatterns=[
    path("user-dashboard/",employee_dashboard, name="user-dashboard"),
    path("manager-dashboard/",manager_dashboard,name="manager-dashboard"),
    path("create-task/", create_task, name="create-task"),
    path("update-task/<int:id>/", update_task, name="update-task"),
    path("delete-task/<int:id>/", delete_task, name="delete-task"),
    path('show-task/', show_tasks)
]