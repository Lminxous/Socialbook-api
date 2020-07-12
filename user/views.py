# General
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Profile
# Rest Framework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
# Google Login
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as googleIdToken
# Repetitive functions written in auth_helpers.py
from user.auth_helpers import generate_random_password,get_jwt_with_user
# System functions
import logging
import sys

viewlog = logging.getLogger('viewlog')

@api_view(['POST',])
def register(request):
    try:
        id_token = request.data['id_token']
    except KeyError:
        viewlog.error(f"{request.path}: no id_token provided in request body. ")
        return Response({'error': 'No id_token provided'}, status=status.HTTP_403_FORBIDDEN)

    id_info = googleIdToken.verify_oauth2_token(id_token, google_requests.Request())

    if id_info['iss'] not in ["accounts.google.com", "https://accounts.google.com"]:
        return Response({'error': "Not a valid Google account"}, status=status.HTTP_403_FORBIDDEN)
    
    email = id_info['email']

    hd = getattr(id_info, 'hd', email.split('@')[-1])
    if hd != 'pilani.bits-pilani.ac.in':
        viewlog.error(f"{request.path}: {email} is not a valid BITS Mail account")
        return Response({'error': 'Not a valid BITS Mail account. '}, status=status.HTTP_403_FORBIDDEN)

    if User.objects.filter(email=email).count() != 0:
        user = User.objects.get(email=email)
        token = get_jwt_with_user(user)
        viewlog.info(f"{request.path}: user {user.username} logged in. ")
        return Response({'token': token}, status=status.HTTP_200_OK)

    user = User(username=email.split('@')[0], email=email) 
    user.set_password(generate_random_password())

    user.save()

    token = get_jwt_with_user(user)

    viewlog.info(f"{request.path}: created user with email {user.email}")
    return Response({'token': token, 'username': user.username, 'email': user.email}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow(request,id):
    profile = Profile.objects.get(id=id)
    if profile not in request.user.profile.follows.all():
        request.user.profile.follows.add(profile)
        viewlog.info(f"{request.path}: You started following {profile}")
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow(request,id):
    profile = Profile.objects.get(id=id)
    if profile in request.user.profile.follows.all():
        request.user.profile.follows.remove(profile)
        viewlog.info(f"{request.path}: You unfollowed {profile}")
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
  