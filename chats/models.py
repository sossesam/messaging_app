from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid

class UserRole(models.TextChoices):
        GUEST = 'GUEST', 'guest'
        HOST = 'HOST', 'host'
        ADMIN = 'ADMIN', 'admin'

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
          if not email or not str(email).strip():
               raise ValueError('Email address required for sign up')
          email = self.normalize_email(email)
          user = self.model(email=email, **extra_fields)
          user.set_password(password)
          user.save(using=self._db)
          return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', UserRole.ADMIN)
        return self.create_user(email, password, **extra_fields)
    

# Create your models here.
class User(AbstractUser):
    username = None
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)
    first_name = models.CharField(null=False)
    last_name = models.CharField(null=False)
    email = models.CharField(unique=True, db_index=True,  null=False, blank=False)
    phone_number = models.CharField(null=True)
    role = models.CharField(max_length=10, choices= UserRole.choices, default=UserRole.GUEST, null=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    objects = CustomUserManager()

    def __str__(self):
         return f"user name: {self.first_name} - {self.last_name}"


class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"conversation - {self.conversation_id}"

class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    conversation = models.ForeignKey(Conversation, default='868a27a1-f511-4a93-b8f0-b1204d8ca9b3', on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"message {self.message_body}"
