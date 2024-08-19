from django.test import TestCase
from .forms import TaskForm
from .models import List

class TaskFormTest(TestCase):
    def setUp(self):
        self.list = List.objects.create(name="Test List", description="A list for testing")

    def test_task_form_valid(self):
        form_data = {
            'title': 'Test Task',
            'description': 'This is a test task.',
            'due_date': timezone.now(),
            'list': self.list.id,
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_form_invalid(self):
        form_data = {
            'title': '',  # title is required
            'description': 'This is a test task.',
            'due_date': timezone.now(),
            'list': self.list.id,
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
