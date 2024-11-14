from django.db import models

# models (pk is setting by default)
class Users(models.Model):
    # users shoudnt be deleted, instead set different status
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    surname = models.CharField(max_length=30, blank=True)
    email = models.CharField(max_length=100)

    # student captain professor
    role = models.TextChoices("Role", "student captain professor")

    status = models.BooleanField(default=True)


class Groups(models.Model):
    group_name = models.CharField(max_length=20)
    professor_id = models.OneToOneField(Users, on_delete=models.DO_NOTHING)


class GroupMembers(models.Model):
    group_id = models.ForeignKey(Groups, on_delete=models.DO_NOTHING)
    student_id = models.ForeignKey(Users, on_delete=models.DO_NOTHING)


class Courses(models.Model):
    course_code = models.CharField(max_length=20)
    course_name = models.CharField(max_length=100)
    institute = models.CharField(max_length=5)
    description = models.TextField()


class CourseTime(models.Model):
    COURSE_TIME = {
        "1": "09:00",
        "2": "10:40",
        "3": "12:40",
        "4": "14:20",
        "5": "16:20",
        "6": "18:00",
    }
    time = models.CharField(max_length=1, choices=COURSE_TIME)


class Enrollments(models.Model):
    student_id = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING)


class Schedules(models.Model):
    course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING)
    professor_id = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    date = models.DateField()
    time = models.ForeignKey(CourseTime, on_delete=models.DO_NOTHING)
    location = models.CharField(max_length=10)
    audience = models.CharField(max_length=10)
    group_id = models.ForeignKey(Groups, on_delete=models.DO_NOTHING)


class Grades(models.Model):
    student_id = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING)
    grade = models.IntegerField()
    grade_type = models.TextChoices("GradeType", "attendence activities achievements test")
    source = models.ForeignKey(Schedules, on_delete=models.DO_NOTHING)
