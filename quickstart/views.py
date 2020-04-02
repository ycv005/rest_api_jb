from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from quickstart.serializers import UserSerializer, GroupSerializer

class UserViewSet(viewsets.ModelViewSet):
    # API endpoint which allow Users to be viewed or edit
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_class = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    # API endpoint which allow groups to be viewed or edit
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_class = [permissions.IsAuthenticated]
