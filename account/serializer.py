from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/
from dotenv import load_dotenv
from django_email_verification import send_email

load_dotenv() 
import os
from verify_email.email_handler import send_verification_email
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import  force_str , force_bytes  
from .utils import generate_token
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import EmailMessage,get_connection
 
import threading
 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
 
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, password):
        validate_password(password)
        return password

    def validate_username(self, username):
        if len(username) < 6:
            raise serializers.ValidationError("The username must be at least 6 characters long.")
        if CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError('User with this Username already exists.')
        return username

    def validate_email(self, email):
        email = email.strip().lower()
 

        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email id already exists.')
        return email
    
    def create(self, validated_data):
 
        user = CustomUser.objects.create_user(**validated_data) 
        user.is_active = False 
        send_email(user)
        return user

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email','username','password')

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        if password:
            instance.set_password(password)
        instance = super().update(instance, validated_data)
 
        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email').lower()
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError("Please give both email and password.")

        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email does not exist.')

        user = authenticate(request=self.context.get('request'), email=email,
                            password=password)
 
        
 
        if not user:
            raise serializers.ValidationError("The login credentials you entered are incorrect or you may need to verify your email. Please check your email for further instructions.")
    
        attrs['user'] = user
        return attrs
 

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
 