from datetime import date

from django.http import HttpResponseRedirect, request
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, FormView, DeleteView

from .forms import TaskForm
from .models import ToDoItem


class AllToDos(ListView):
    model = ToDoItem
    template_name = "todo/index.html"

    def get_queryset(self):
        return ToDoItem.objects.filter(due_date__gte=date.today())


class TodayToDos(ListView):
    model = ToDoItem
    template_name = "todo/today.html"

    def get_queryset(self):
        return ToDoItem.objects.filter(due_date=date.today())


class AddTask(FormView):
    template_name = "todo/add-task.html"
    form_class = TaskForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class DeleteTask(View):
    def post(self, request):
        todo_ids = request.POST.getlist('todo_ids')

        ToDoItem.objects.filter(id__in=todo_ids).delete()

        return HttpResponseRedirect(reverse_lazy('index'))