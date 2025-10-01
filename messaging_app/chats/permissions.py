from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsParticipantOfConversation(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated #will be allowing only the logged-in users