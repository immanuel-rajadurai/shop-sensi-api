# Generated by Django 5.0.2 on 2024-03-30 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_answerset'),
    ]

    operations = [
        migrations.AddField(
            model_name='answerset',
            name='answers',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]
