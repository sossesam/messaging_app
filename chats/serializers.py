from rest_framework import serializers
from .models import Conversation, Message
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="A user with this email address already exists."
            )
        ]
    )
    class Meta:
        model = User
        fields = ('user_id', 'first_name', 'last_name', 'email', 'password', 'phone_number', 'role')
        read_only_fields = ['user_id']
        extra_kwargs = {
            'password': {'write_only': True}  # Ensures password isn't leaked in responses
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        return User.objects.create_user(password=password, **validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role')
        


class UsersSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['user_id','first_name', 'last_name', 'email', 'password','phone_number', 'role', 'password']
        

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
   

    

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['message_id']


class MessageCreateSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )
    class Meta:
        model = Message
        fields = ['sender', 'message_body']
        read_only_fields = ['id', 'created_at']
        


class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        allow_empty=False
    )

    class Meta:
        model = Conversation
        fields = '__all__'
        read_only_fields=['conversation_id']

    def validate_participants(self, value):
        # Optional: Custom logic to ensure user isn't creating a chat with non-existent users
        if len(value) < 1:
            raise serializers.ValidationError("You must specify at least one participant.")
        return value

    def to_representation(self, instance):
        # Expands participant IDs into full user objects on responses
        representation = super().to_representation(instance)
        representation['participants'] = UsersSerializer(
            instance.participants.all(), 
            many=True
        ).data
        representation['messages'] = MessageSerializer(
            instance.messages.all(),
            many=True
        ).data
        return representation

class ConversationDetailSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    participants = UsersSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']


