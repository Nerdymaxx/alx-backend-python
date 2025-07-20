from rest_framework import serializers;
from django.contrib.auth.models import Group, User
from .models import User, Conversation , Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name',  'last_name', 'email', 'phone_number', 'role','timestamp']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'timestamp']


class ConversationSerializer(serializers.ModelSerializer):
    participants =UserSerializer(many=True, read_only = True)
    messages= MessageSerializer(many =True, read_only= True)
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'timestamp']
