from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsParticipantOfConversation(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated #will be allowing only the logged-in users
    
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()
        elif isinstance(obj, Message):
            return request.user in obj.conversation.participants.all() 
        return False