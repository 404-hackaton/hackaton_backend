# Generated by Django 5.1.3 on 2024-11-14 16:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_code', models.CharField(max_length=20)),
                ('course_name', models.CharField(max_length=100)),
                ('institute', models.CharField(max_length=5)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CourseTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.CharField(choices=[('1', '09:00'), ('2', '10:40'), ('3', '12:40'), ('4', '14:20'), ('5', '16:20'), ('6', '18:00')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=128)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('surname', models.CharField(blank=True, max_length=30)),
                ('email', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Schedules',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('location', models.CharField(max_length=10)),
                ('audience', models.CharField(max_length=10)),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='base.courses')),
                ('group_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='base.groups')),
                ('time', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='base.coursetime')),
                ('professor_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='base.users')),
            ],
        ),
        migrations.AddField(
            model_name='groups',
            name='professor_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='base.users'),
        ),
        migrations.CreateModel(
            name='GroupMembers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='base.groups')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='base.users')),
            ],
        ),
        migrations.CreateModel(
            name='Grades',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.IntegerField()),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='base.courses')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='base.schedules')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='base.users')),
            ],
        ),
        migrations.CreateModel(
            name='Enrollments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='base.courses')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='base.users')),
            ],
        ),
    ]
