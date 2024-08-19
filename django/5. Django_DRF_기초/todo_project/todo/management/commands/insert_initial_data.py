from django.core.management.base import BaseCommand
from todo.models import Todo

class Command(BaseCommand):
    help = 'Insert initial data into the Todo model'

    def handle(self, *args, **kwargs):
        Todo.objects.create(title='Learn Django', description='Start with Django basics', is_completed=False)
        Todo.objects.create(title='Build API', description='Create a REST API with Django', is_completed=False)
        self.stdout.write(self.style.SUCCESS('Successfully inserted initial data into the Todo model'))
