# Generated by Django 5.1.3 on 2024-11-18 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_attendence'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='first_enter',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='last_enter',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='attendence',
            unique_together={('student', 'source')},
        ),
    ]