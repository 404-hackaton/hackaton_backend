# Generated by Django 5.1.3 on 2024-11-18 07:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedule',
            old_name='group',
            new_name='groups',
        ),
        migrations.AlterUniqueTogether(
            name='groupmember',
            unique_together={('group', 'student')},
        ),
    ]