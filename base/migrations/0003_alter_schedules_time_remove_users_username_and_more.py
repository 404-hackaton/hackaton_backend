# Generated by Django 5.1.3 on 2024-11-14 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_groups_professor_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedules',
            name='time',
            field=models.CharField(choices=[('1', '09:00'), ('2', '10:40'), ('3', '12:40'), ('4', '14:20'), ('5', '16:20'), ('6', '18:00')], max_length=1),
        ),
        migrations.RemoveField(
            model_name='users',
            name='username',
        ),
        migrations.DeleteModel(
            name='CourseTime',
        ),
    ]