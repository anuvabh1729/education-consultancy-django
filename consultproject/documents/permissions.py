# documents/permissions.py
from rest_framework.permissions import BasePermission


class IsConsultantOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["consultant", "admin"]


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "student"
