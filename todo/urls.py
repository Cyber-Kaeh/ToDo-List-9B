from django.urls import path
from . import views

urlpatterns = [
    path("", views.AllToDos.as_view(), name="index"),
    path("today/", views.TodayToDos.as_view(), name="today"),
    path("add-task/",views.AddTask.as_view(), name="add_task"),
    path("delete-todos/",views.DeleteTask.as_view(), name="delete_todos"),
]
