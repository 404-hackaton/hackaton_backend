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
    })
    status = models.BooleanField(default=True)

    # get all members of the groups this user belongs to.
    def get_all_group_members(self):
        return User.objects.filter(
            group_memberships__group_id__in=self.group_memberships.values('group_id')
        ).distinct()

    def get_group_id(self):
        return self.group_memberships.values('group_id')

    def get_schedule_day(self, date):
        schedules = Schedule.objects.filter(group__members__student=self.id, date=date).distinct()
        return schedules
        
    def get_id(self):
        return self.id

    def __str__(self):
        return self.email + " | " + str(self.id) + " | " + self.role[0]


class Group(models.Model):
    group_name = models.CharField(max_length=20, unique=True)
    professor = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.group_name


class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, related_name="members")
    student = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="group_memberships")

    class Meta:
        unique_together = ["group", "student"]


class Course(models.Model):
    course_name = models.CharField(max_length=100)
    course_type = models.CharField(max_length=20, blank=True)
    institute = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ["course_name", "course_type", "institute"]

    def __str__(self):
        return self.course_name + " | " + self.course_type


# class Subject(model.Model):
#     subject_name = models.CharField()

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ["student", "course"]


class Schedule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    professor = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateField()
    time = models.CharField(max_length=1, choices=COURSE_TIME)
    location = models.CharField(max_length=10, choices=LOCATIONS)
    audience = models.CharField(max_length=10)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, blank=True)

    class Meta:
        unique_together = ["date", "time", "audience", "location"]


class Grade(models.Model):
    student = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    grade = models.IntegerField()
    grade_type = models.CharField(max_length=15, choices={
        "ATTENDENCE": 'attendence',
        "ACTIVITIES": "activities",
        "ACHIEVMENTS": "achievments",
        "TEST": "test",
    })
    source = models.ForeignKey(Schedule, on_delete=models.DO_NOTHING)

class Token(models.Model):
    token = models.CharField(max_length=10, unique=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    token_created = models.DateTimeField()


# TODO: clean this shit out of trash (blank)