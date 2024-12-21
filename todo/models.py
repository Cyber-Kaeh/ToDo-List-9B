from django.db import models
from django.utils import timezone

# Create your models here.
class ToDoItem(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=100)
    due_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.text}: due {self.due_date}"

