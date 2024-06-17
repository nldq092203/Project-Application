from rest_framework import serializers
from . import models
from django.utils import timezone
from rest_framework.validators import UniqueTogetherValidator

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Participant
        fields = ['id', 'username', 'first_name', 'last_name', 'organization', 'image', 'role']

class GroupRunnerSerializer(serializers.ModelSerializer):
    members = serializers.HyperlinkedRelatedField(
        many=True,
        queryset=models.Participant.objects.all(),
        view_name='participant-detail',
    )
    class Meta:
        model = models.GroupRunner
        fields = ['name', 'members']

class EventSerializer(serializers.ModelSerializer):
    coach = serializers.HyperlinkedRelatedField(
        view_name='participant-detail',
        queryset=models.Participant.objects.all()
    )
    GroupRunner = serializers.HyperlinkedRelatedField(
        view_name='group-runner-detail',
        queryset=models.GroupRunner.objects.all()
    )

    def validate(self, attrs):
        if attrs['start'] > attrs['end']:
            raise serializers.ValidationError("End date must be later than start date")
        if attrs['start'] < timezone.now():
            raise serializers.ValidationError("Start date must be later than current date")
        return super().validate(attrs)
        
    class Meta:
        model = models.Event
        fields = ['name', 'start', 'end', 'location', 'coach', 'group_runner', 'publish', 'subtitle', 'description', 'image', 'organization']

class RaceSerializer(serializers.ModelSerializer):
    event = serializers.HyperlinkedRelatedField(
        view_name='event-detail',
        queryset=models.Event.objects.all()
    )

    def validate(self, attrs):
        if attrs['time_limit'] > attrs['event'].end - attrs['event'].start:
            raise serializers.ValidationError("Time limit must be less than event duration")
        if attrs['time_limit'] < 0:
            raise serializers.ValidationError("Time limit must be positive")
        
        return super().validate(attrs)

    class Meta:
        model = models.Race
        fields = ['name', 'event', 'time_limit', 'type']

class RaceRunnerSerializer(serializers.ModelSerializer):
    runner = serializers.HyperlinkedRelatedField(
        view_name='participant-detail',
        queryset=models.Participant.objects.all()
    )

    race = serializers.HyperlinkedRelatedField(
        view_name='race-detail',
        queryset = models.Race.objects.all()
    )

    def validate(self, attrs):
        if attrs['total_time'] < 0:
            raise serializers.ValidationError("Total time must be positive")
        if attrs['score'] < 0:
            raise serializers.ValidationError("Score must be positive")
        return super().validate(attrs)
    
    class Meta:
        model = models.RaceRunner
        fields = ['runner', 'race', 'total_time', 'score']

class CheckPointSerializer(serializers.ModelSerializer):
    race = serializers.HyperlinkedRelatedField(
        view_name='race-detail',
        queryset = models.Race.objects.all()
    )

    class Meta:
        model = models.CheckPoint
        fields = ['number', 'location', 'race']
        validators = [
            UniqueTogetherValidator(
                queryset=models.CheckPoint.objects.all(),
                fields=['number', 'race']
            )
        ]
                  