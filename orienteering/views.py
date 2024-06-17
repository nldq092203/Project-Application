from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import Group
from djoser.views import UserViewSet, TokenCreateView, TokenDestroyView
from rest_framework.response import Response
from rest_framework import status, generics
from djoser import utils
from djoser.compat import get_user_email
from djoser.conf import settings
from rest_framework.permissions import IsAdminUser, IsAuthenticated, BasePermission
from .models import Participant, GroupRunner, Event, RaceType, Race, CheckPoint, RaceRunner
from .serializers import ParticipantSerializer, GroupRunnerSerializer, EventSerializer, RaceRunnerSerializer, RaceSerializer, CheckPointSerializer


############################Authorization and Authentication#################################
# Register
class CustomParticipantCreateView(UserViewSet): 
    def create(self, request, *args, **kwargs):
        role = request.data.get('role', 'Runner')
        code_secret = request.data.get('secret_code')
        if not code_secret and role == 'Coach':
            return Response({"message": "Secret code is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        COACH_SECRET_CODE = settings.COACH_SECRET_CODE

        if role == 'Coach' and code_secret != COACH_SECRET_CODE:
            return Response({"message": "Invalid secret code."}, status=status.HTTP_400_BAD_REQUEST)
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            user = Participant.objects.get(username=response.data['username'])
            if role == 'Coach':
                group = Group.objects.get(name='Coach')
                user.groups.add(group)
            elif role == 'Runner':
                group = Group.objects.get(name='Runner')
                user.groups.add(group)
            custom_data = {"message": "Participant created successfully", "data": response.data, "role": role}  
            return Response(custom_data, status=status.HTTP_201_CREATED)
        return response
    
# Login
class CustomTokenCreateView(TokenCreateView):
    def _action(self, serializer):
        token = super(CustomTokenCreateView, self)._action(serializer)
        return Response({
            'message': 'Login successfully',
            'accessToken': token.data['auth_token'],
        })

# Logout
class CustomTokenDestroyView(TokenDestroyView):
    def post(self, request):
        utils.logout_user(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

# Request for resetting password when forgetting
class RequestPasswordResetView(UserViewSet):
    def reset_password(self, request, *args, **kwargs):
        super().reset_password(request, *args, **kwargs)
        return Response({'message': 'Send reset password request successful'},status=status.HTTP_200_OK)

# Confirm New Password
class ConfirmPasswordResetView(UserViewSet):
    def reset_password_confirm(self, request, *args, **kwargs):
        super().reset_password_confirm(request, *args, kwargs)
        return Response({'message': 'Confirm reset password successful'},status=status.HTTP_200_OK)

# Set New Password (Authenticated User)
class SetPassword(UserViewSet):
    def set_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()

        if settings.PASSWORD_CHANGED_EMAIL_CONFIRMATION:
            context = {"user": self.request.user}
            to = [get_user_email(self.request.user)]
            settings.EMAIL.password_changed_confirmation(self.request, context).send(to)

        logout_session = self.request.data.get('logout_after_password_change', False)
        if logout_session:
            utils.logout_user(self.request)
        elif settings.CREATE_SESSION_ON_LOGIN:
            update_session_auth_hash(self.request, self.request.user)
        return Response({'message': 'Set password successful', 'logout':logout_session},status=status.HTTP_200_OK)


class IsCoach(BasePermission):
    def has_permission(self,request, view):
        if request.user:
            return request.user.groups.filter(name="Coach")
        return False

class IsRunner(BasePermission):
    def has_permission(self,request, view):
        if request.user:
            return request.user.groups.filter(name="Runner")
        return False
    
############################App Logics############################

# class EventCoachView(generics.ListCreateAPIView):
#     serializer_class = EventSerializer

#     def get_permissions(self):
#         return [IsCoach()]
    
#     def get_queryset(self):
#         user = self.request.user
#         my_manage_events = Event.objects.filter(coach=user).order_by('-start')
#         return my_manage_events
    
#     def create(self, request, *args, **kwargs):
#         data = request.data.copy()
#         data['coach'] = self.request.user.id
#         event_serializer = EventSerializer(data=data)

#         if event_serializer.is_valid():
#             event_serializer.save()
#             return Response(event_serializer.data, status=status.HTTP_201_CREATED)
#         return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class EventParticipateView(generics.ListAPIView):
#     serializer_class = EventSerializer
#     search_fields = ['group_runner__name', 'is_finished']
#     ordering_fields = ['-start', 'start', 'end', '-end']
#     def get_permissions(self):
#         return [IsRunner()]
    
#     def get_queryset(self):
#         runner = self.request.user
#         group_runners = GroupRunner.objects.filter(members=runner)
#         my_participate_events = Event.objects.filter(group_runner__in=group_runners).order_by('-start')
#         return my_participate_events


    