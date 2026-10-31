from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .serializers import MessageSerializer, ConversationSerializer, UsersSerializer, ConversationDetailSerializer, MessageCreateSerializer, RegisterSerializer, UserProfileSerializer, LoginSerializer
from .models import Message, Conversation, User
from .permissions import IsParticipantOfConversation
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken

from django.shortcuts import get_object_or_404
# Create your views here.

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = []

class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get_object(self):
        return self.request.user



class ConversationListAndCreateAPIView(APIView):
    serializer_class = ConversationSerializer
    def get(self, request):
        conversation = Conversation.objects.filter(participants=request.user)
        serialized_conversation = self.serializer_class(conversation, many=True)
        return Response(serialized_conversation.data, status=status.HTTP_200_OK)

    def post(self, request):
        serialize_conversation = self.serializer_class(data=request.data)
        if serialize_conversation.is_valid():
            serialize_conversation.save()
            return Response(serialize_conversation.data, status=status.HTTP_201_CREATED)
        return Response(serialize_conversation.errors, status=status.HTTP_400_BAD_REQUEST)


class ParticipantListAndCreateAPIView(APIView):
    serializer_class = UsersSerializer
    def get(self, request):
        particpant = User.objects.all()
        serialized_participants = self.serializer_class(particpant, many=True)
        return Response(serialized_participants.data, status=status.HTTP_200_OK)

class MessageListAndCreateAPIView(APIView):
    serializer_class = MessageSerializer
    def post(self, request):
        serialized_messages = self.serializer_class(data=request.data)
        if serialized_messages.is_valid():
            serialized_messages.save()
            return Response(serialized_messages.data, status=status.HTTP_200_OK)
        return Response(serialized_messages.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        messages = Message.objects.all()
        serialized_messages = self.serializer_class(messages, many=True)
        return Response(serialized_messages.data, status=status.HTTP_200_OK)


class ConversationDetailAPIView(APIView):
    def get_object(self, pk):
        """Helper method to fetch conversation or return 404."""
        return get_object_or_404(Conversation, pk=pk)

    def get(self, request, pk):
        """Retrieve a single conversation details."""
        conversation = self.get_object(pk)
        self.check_object_permissions(request, conversation)
        serializer = ConversationDetailSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ConversationMessagesAPIView(APIView):
    permission_classes = []
    serializer_class = MessageCreateSerializer
    def get(self, request, conversation_pk):
        """List all messages for this specific conversation."""
        conversation = get_object_or_404(Conversation, pk=conversation_pk)
        messages = conversation.messages.all()
        serializer = MessageCreateSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, conversation_pk):
        """Create a new message inside this conversation."""
        conversation = get_object_or_404(Conversation, pk=conversation_pk)
        serialized_messages = self.serializer_class(data=request.data)
        
        if serialized_messages.is_valid():
            # Automatically assign the conversation instance from the URL
            serialized_messages.save(conversation=conversation)
            return Response(serialized_messages.data, status=status.HTTP_201_CREATED)
        return Response(serialized_messages.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    def post(self, request):
        serialized_login = self.serializer_class(data=request.data)
        if serialized_login.is_valid():
            email = serialized_login.validated_data['email']
            password = serialized_login.validated_data['password']
           

            # Authenticate against CustomUser model using primary hasher (Bcrypt)
            user = authenticate(request, username=email, password=password)
        
        if user is not None :
            login(request, user)  # Creates session & attaches sessionid cookie
            session_key = request.session.session_key
            
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful',
                'user': UserProfileSerializer(user).data,
                'session_key': session_key,
                'tokens': {
                    'refresh': str(refresh),               # <--- Add str() here
                    'access': str(refresh.access_token),   # <--- Add str() here
                    }
                
            }, status=status.HTTP_200_OK)

        return Response(
            {'error': 'Invalid email or password'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)  # Destroys session & flushes cookie
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)