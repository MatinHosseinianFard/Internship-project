from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TaskManager(models.Manager):
    def related_tasks_to_charity(self, user):
        return self.filter(charity__user=user)

    def related_tasks_to_benefactor(self, user):
        return self.filter(assigned_benefactor__user=user)

    def all_related_tasks_to_user(self, user):
        return self.filter(models.Q(charity__user=user) |
                           models.Q(assigned_benefactor__user=user) |
                           models.Q(state='P'))


class Benefactor(models.Model):
    EXPERIENCE_CHOICES = (
        (0, 'Beginner'),
        (1, 'Intermediate'),
        (2, 'Expert'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience = models.SmallIntegerField(
        choices=EXPERIENCE_CHOICES, default=0)
    free_time_per_week = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.user.username


class Charity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    reg_number = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Task(models.Model):

    objects = TaskManager()

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    STATE_CHOICES = (
        ('P', 'Pending'),
        ('W', 'Waiting'),
        ('A', 'Assigned'),
        ('D', 'Done'),
    )
    assigned_benefactor = models.ForeignKey(
        Benefactor, on_delete=models.SET_NULL, null=True, blank=True)
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE)
    age_limit_from = models.IntegerField(blank=True, null=True)
    age_limit_to = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    gender_limit = models.CharField(
        max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    state = models.CharField(max_length=1, choices=STATE_CHOICES, default='P')
    title = models.CharField(max_length=60)

    def __str__(self):
        return self.title
