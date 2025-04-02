from django.urls import path
from task.views import user_dashboard,manager_dashboard,test,create_task,show_tasks,update_task

urlpatterns=[
    path("user-dashboard/",user_dashboard, name="user-dashboard"),
    path("manager-dashboard/",manager_dashboard,name="manager-dashboard"),
    path("test/",test),
    path("create-task/", create_task, name="create-task"),
    path("update-task/<int:id>/", update_task, name="update-task"),
    path('show-task/', show_tasks)
]