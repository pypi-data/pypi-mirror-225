from rest_framework.permissions import BasePermission


class HasCreateProjectConsentTokenPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('project_consents.add_projectconsenttoken')
