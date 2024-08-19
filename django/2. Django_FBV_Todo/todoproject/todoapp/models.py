from django.test import TestCase
from .models import Task, List
from django.utils import timezone

class TaskModelTest(TestCase):
    def setUp(self):
        self.list = List.objects.create(name="Test List", description="A list for testing")
        self.task = Task.objects.create(
            title="Test Task",
            description="This is a test task.",
            due_date=timezone.now(),
            list=self.list,
            priority=2
        )

    def test_task_str(self):
        self.assertEqual(str(self.task), "Test Task (우선순위: 중간)")

    def test_priority_choices(self):
        self.assertEqual(self.task.get_priority_display(), "중간")

    def test_task_creation(self):
        self.assertEqual(Task.objects.count(), 1)
