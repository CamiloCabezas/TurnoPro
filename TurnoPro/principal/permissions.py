from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Permite acceso solo a usuarios con rol 'admin'.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.rol == 'admin')


class IsEmpresa(permissions.BasePermission):
    """
    Permite acceso solo a usuarios con rol 'empresa'.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.rol == 'empresa')


class IsEmpleado(permissions.BasePermission):
    """
    Permite acceso solo a usuarios con rol 'empleado'.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.rol == 'empleado')