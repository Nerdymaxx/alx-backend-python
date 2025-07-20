from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer



# Create your views here.
class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classees= [permissions.IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(participants =self.request.user)
    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    queryset= Message.objects.all().order_by('timestamp')
    serializer_class = MessageSerializer 
    permission_classes = [permissions.IsAuthenticated]   

    def get_queryset(self):
        return Message.objects.filter(sender = self.request.user).get_queryset()