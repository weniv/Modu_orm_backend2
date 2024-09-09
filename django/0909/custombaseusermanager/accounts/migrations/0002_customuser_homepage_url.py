# Generated by Django 5.1.1 on 2024-09-09 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='homepage_url',
            field=models.URLField(default='http://hello.com', verbose_name='homepage URL'),
            preserve_default=False,
        ),
    ]
