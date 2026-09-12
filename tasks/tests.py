from django.test import TestCase
from .models import Task

class TaskModelTests(TestCase):
    def test_task_defaults(self):
        task = Task.objects.create(title="Follow up call")
        self.assertEqual(task.priority, 'medium')
        self.assertFalse(task.is_completed)