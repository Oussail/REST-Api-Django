from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated

from . import serializers
from . import models
from . import permissions

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profiles."""

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields= ('name', 'email',)


class LoginViewSet(viewsets.ViewSet):
    """Checks Email and password and retuens an auth token"""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """ Use The ObtainAuthenToken APIViews to validate and create a token """

        return ObtainAuthToken().post(request)


class UserProfileFeedViewset(viewsets.ModelViewSet):
    """ Handles creating, reading and updating profiles feed item"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.PostOwnStatus, IsAuthenticated)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user."""
        serializer.save(user_profile=self.request.user)
