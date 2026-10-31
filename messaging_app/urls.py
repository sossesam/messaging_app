"""
URL configuration for messaging_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from chats.views import ConversationListAndCreateAPIView, ParticipantListAndCreateAPIView, MessageListAndCreateAPIView, ConversationDetailAPIView, ConversationMessagesAPIView, RegisterView, UserProfileView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('chats.urls')),
    path('participants', ParticipantListAndCreateAPIView.as_view(), name="participants-list-create"),
    path('messages', MessageListAndCreateAPIView.as_view(), name='messages-list-create'),
    path('conversations', ConversationListAndCreateAPIView.as_view(), name="conversation-list-create"),
    path('conversations/<uuid:pk>/', ConversationDetailAPIView.as_view(), name='conversation-detail'),
    path('conversations/<uuid:conversation_pk>/messages/', ConversationMessagesAPIView.as_view(), name='conversation-messages'),
    path('api-auth/', include('rest_framework.urls'))
]

