from django.test import TestCase
from django.urls import reverse
from .models import Task, List

class TaskListViewTest(TestCase):
    def setUp(self):
        self.list = List.objects.create(name="Test List", description="A list for testing")
        self.task = Task.objects.create(
            title="Test Task",
            description="This is a test task.",
            list=self.list,
            priority=2
        )

    def test_task_list_view_status_code(self):
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)

    def test_task_list_view_template(self):
        response = self.client.get(reverse('task_list'))
        self.assertTemplateUsed(response, 'todoapp/task_list.html')

    def test_task_list_view_content(self):
        response = self.client.get(reverse('task_list'))
        self.assertContains(response, self.task.title)

class TaskStatisticsViewTest(TestCase):
    def setUp(self):
        self.list = List.objects.create(name="Test List", description="A list for testing")
        Task.objects.create(title="Test Task 1", list=self.list, priority=1, completed=True)
        Task.objects.create(title="Test Task 2", list=self.list, priority=2, completed=False)
        Task.objects.create(title="Test Task 3", list=self.list, priority=3, completed=True)

    def test_task_statistics_view_status_code(self):
        response = self.client.get(reverse('task_statistics'))
        self.assertEqual(response.status_code, 200)

    def test_task_statistics_calculations(self):
        response = self.client.get(reverse('task_statistics'))
        statistics = response.context['statistics']
        self.assertEqual(statistics['total_tasks'], 3)
        self.assertEqual(statistics['completed_tasks'], 2)
        self.assertEqual(statistics['incomplete_tasks'], 1)
        self.assertEqual(statistics['high_priority_tasks'], 1)
        self.assertEqual(statistics['medium_priority_tasks'], 1)
        self.assertEqual(statistics['low_priority_tasks'], 1)
        self.assertEqual(statistics['priority_1_completion_rate'], 100)
        self.assertEqual(statistics['priority_2_completion_rate'], 0)
        self.assertEqual(statistics['priority_3_completion_rate'], 100)
