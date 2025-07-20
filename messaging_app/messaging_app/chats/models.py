from django.db import models
import uuid

# USER MODEL
class User(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    # Use choices for 'role'
    ROLE_CHOICES = (
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# CONVERSATION MODEL
class Conversation(models.Model):  # corrected 'models.model' -> 'models.Model'
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)
    participants = models.ManyToManyField(User)  # Use ManyToManyField to support group chats
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


# MESSAGE MODEL
class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)  # Only use auto_now_add for creation time

    def __str__(self):
        return f"Message from {self.sender.email}"
