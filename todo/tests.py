from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse
from .models import ToDoItem
from todo.forms import TaskForm


def create_todo(todo_text, days):
    return ToDoItem.objects.create(text=todo_text, due_date=date.today() + timedelta(days=days))

# Test the dates to ensure there are no old todos
class AllToDosViewTest(TestCase):

    def test_today(self):
        todo = create_todo("To be done today", 0)
        response = self.client.get(reverse("index"))
        self.assertQuerySetEqual(
            response.context["todoitem_list"],
            [todo]
        )

    def test_last_week(self):
        todo = create_todo("This task is past due", -7)
        response = self.client.get(reverse("index"))
        self.assertQuerySetEqual(
            response.context["todoitem_list"],
            []
        )

    def test_next_week(self):
        todo = create_todo("Still have some time", 7)
        response = self.client.get(reverse("index"))
        self.assertQuerySetEqual(
            response.context["todoitem_list"],
            [todo]
        )


# Test if the form is functioning properly
class TaskFormTest(TestCase):

    def test_task_form_valid(self):
        form_data = {
            "text": "Task test today",
            "due_date": date.today()
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    # Make sure there are no entries without a desc.
    def test_task_form_invalid(self):
        form_data = {
            "due_date": date.today()
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("text", form.errors)


# Integration Test for entire workflow
class AddTaskViewTest(TestCase):
    def test_add_task_view_get(self):
        """
        Test if the AddTask view renders the form correctly
        """
        response = self.client.get(reverse("add_task"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todo/add-task.html")
        self.assertContains(response, "<form")

    def test_add_task_view_post_valid(self):
        """
        Test if the AddTask view successfully creates a new task
        when valid data is submitted
        """
        form_data = {
            "text": "New Task",
            "due_date": date.today() + timedelta(days=1),
        }
        response = self.client.post(reverse("add_task"), data=form_data)

        self.assertEqual(ToDoItem.objects.count(), 1)
        task = ToDoItem.objects.first()
        self.assertEqual(task.text, "New Task")
        self.assertEqual(task.due_date, date.today() + timedelta(days=1))

        self.assertRedirects(response, reverse("index"))

    def test_add_task_view_post_invalid(self):
        """
        Test if the AddTask view re-renders the form with errors
        when invalid data is submitted
        """
        form_data = {
            "due_date": date.today() + timedelta(days=1),
        }
        response = self.client.post(reverse("add_task"), data=form_data)

        self.assertEqual(ToDoItem.objects.count(), 0)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todo/add-task.html")
        self.assertContains(response, "This field is required.")
