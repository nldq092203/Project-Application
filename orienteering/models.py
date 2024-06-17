from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.auth.models import AbstractUser, Group, Permission


class Participant(AbstractUser):
    organization = models.CharField(max_length=100)
    image = models.ImageField(upload_to='profile_images', blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')
    
class GroupRunner(models.Model):
    name = models.CharField(max_length=50)
    members = models.ManyToManyField(Participant, related_name='member_group_runners')

    def __str__(self):
        return self.name
    
class Event(models.Model):
    name = models.CharField(max_length=100)
    start = models.DateTimeField()
    end = models.DateTimeField()
    location = models.CharField(max_length=100)
    coach = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='events')
    group_runner = models.ForeignKey(GroupRunner, on_delete=models.CASCADE, related_name='events')
    publish = models.BooleanField(default=False)
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='event_images', blank=True, null=True)
    organization = models.CharField(max_length=100, blank=True, null=True)
    is_finished = models.BooleanField(default=False)

class RaceType(models.Model):
    name = models.CharField(max_length=100)
    rule = models.TextField()

    def __str__(self):
        return self.name
    
class Race(models.Model):
    name = models.CharField(max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="races")
    time_limit = models.DurationField()
    race_type = models.ForeignKey(RaceType, on_delete=models.CASCADE, related_name='races')

class CheckPoint(models.Model):
    number = models.IntegerField()
    location = gis_models.PointField()
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='checkpoints')

class RaceRunner(models.Model):
    runner = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="race_runners")
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name="race_runners")
    total_time = models.DurationField(blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)



    
