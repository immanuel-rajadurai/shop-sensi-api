# Generated by Django 5.0.2 on 2024-03-16 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_questionset_questions_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionset',
            name='questions',
            field=models.CharField(default='default_question', max_length=10000),
        ),
    ]
