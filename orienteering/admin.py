from django.contrib import admin
from . import models

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'organization', 'email']
    search_fields = ['username', 'first_name', 'last_name', 'organization']
    list_filter = ['organization']
    fieldsets = [
        (None, {'fields': ['username', 'password']}),
        ('Personal info', {'fields': ['first_name', 'last_name', 'organization', 'image', 'email']}),
    ]

class GroupRunnerAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    filter_horizontal = ['members']

class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'start', 'end', 'location', 'coach', 'group_runner', 'publish']
    search_fields = ['name', 'location', 'coach', 'group_runner']
    list_filter = ['publish']
    fieldsets = [
        (None, {'fields': ['name', 'start', 'end', 'location', 'coach', 'group_runner', 'publish']}),
        ('Description', {'fields': ['subtitle', 'description', 'image', 'organization']}),
    ]

class RaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'event', 'time_limit', 'race_type']
    search_fields = ['name', 'event', 'race_type']
    list_filter = ['race_type']
    fieldsets = [
        (None, {'fields': ['name', 'event', 'time_limit', 'race_type']}),
    ]

class CheckPointAdmin(admin.ModelAdmin):
    list_display = ['number', 'location', 'race']
    search_fields = ['number', 'race']
    list_filter = ['race']

class RaceRunnerAdmin(admin.ModelAdmin):
    list_display = ['runner', 'race', 'total_time', 'score']
    search_fields = ['runner', 'race']
    list_filter = ['race', 'runner']

class RaceTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

admin.site.register(models.Participant, ParticipantAdmin)
admin.site.register(models.GroupRunner, GroupRunnerAdmin)
admin.site.register(models.Event, EventAdmin)
admin.site.register(models.Race, RaceAdmin)
admin.site.register(models.CheckPoint, CheckPointAdmin)
admin.site.register(models.RaceRunner, RaceRunnerAdmin)
admin.site.register(models.RaceType, RaceTypeAdmin)

