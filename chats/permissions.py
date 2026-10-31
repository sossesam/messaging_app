from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Object-level permission to only allow participants of a conversation to access it.
    """
    def has_permission(self, request, view):
        # Ensure the user is logged in
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Assumes Conversation model has a ManyToManyField named 'participants'
        return obj.participants.filter(id=request.user.id).exists()