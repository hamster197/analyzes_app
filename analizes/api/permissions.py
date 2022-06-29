from rest_framework import permissions

from analizes.decorators import *


class IsAdminOrDoctorsReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if doctor_check(request.user):
            if request.method in permissions.SAFE_METHODS:
                return True
        return admin_check(request.user)

class IsAdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return admin_check(request.user)

class AuthorOrDoctorsReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if doctor_check(request.user) or request.user.pk == obj.pk:
            if request.method in permissions.SAFE_METHODS:
                return True

class IsDoctorOrPatientReadOnly(permissions.BasePermission):

    def has_permission(self, request, view, ):
        if patients_check(request.user):
            if request.user == get_object_or_404(User, pk=view.kwargs.get('pk')):
                if request.method in permissions.SAFE_METHODS:
                    return True
        if doctor_check(request.user):
            if get_object_or_404(User, pk=view.kwargs.get('pk')).groups.get().name == 'patients':
                return True


