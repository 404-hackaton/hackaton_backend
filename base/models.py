from django.db import models


COURSE_TIME = {
    "1": "09:00",
    "2": "10:40",
    "3": "12:40",
    "4": "14:20",
    "5": "16:20",
    "6": "18:00",
}
LOCATIONS = {
    "В-86": "Проспект Вернадского 86",
    "МП-1": "Малвя Пироговская 1",
    "СТ-17": "Стромынкина 17"
}



# models (pk is setting by default)
class User(models.Model):
    # users shoudnt be deleted, instead set different status
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    surname = models.CharField(max_length=30, blank=True)
    role = models.CharField(max_length=15, choices={
        "STUDENT": "student",
        "CAPTAIN": "captain",
        "PROFESSOR": "professor",
        "ADMINISTRATOR": "administrator",
    }, blank=True)
    status = models.BooleanField(default=True)

    # get all members of the groups this user belongs to.
    def get_all_group_members(self):
        return User.objects.filter(
            group_memberships__group_id__in=self.group_memberships.values('group_id')
        ).distinct()
    
    def get_group_id(self):
        return self.group_memberships.values('group_id')

    def __str__(self):
        return self.email + " | " + str(self.id)


class Group(models.Model):
    group_name = models.CharField(max_length=20, unique=True)
    professor_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.group_name


class GroupMember(models.Model):
    group_id = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    student_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="group_memberships")


class Course(models.Model):
    course_name = models.CharField(max_length=100, unique=True)
    course_type = models.CharField(max_length=20, blank=True)
    institute = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.course_name


# class Subject(model.Model):
#     subject_name = models.CharField()

class Enrollment(models.Model):
    student_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    course_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ["student_id", "course_id"]


class Schedule(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    professor_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateField()
    time = models.CharField(max_length=1, choices=COURSE_TIME)
    location = models.CharField(max_length=10, choices=LOCATIONS)
    audience = models.CharField(max_length=10)
    group_id = models.ForeignKey(Group, on_delete=models.DO_NOTHING, blank=True)

    class Meta:
        unique_together = ["date", "time", "audience", "location"]


class Grade(models.Model):
    student_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    course_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    grade = models.IntegerField()
    grade_type = models.CharField(max_length=15, choices={
        "ATTENDENCE": 'attendence',
        "ACTIVITIES": "activities",
        "ACHIEVMENTS": "achievments",
        "TEST": "test",
    }, blank=True)
    source = models.ForeignKey(Schedule, on_delete=models.DO_NOTHING)


# TODO: clean this shit out of trash (blank)