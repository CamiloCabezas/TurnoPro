from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Movimientos, Usuario
from .serializers import MovimientosSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .permissions import IsAdmin, IsEmpleado, IsEmpresa


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):

        try:
            response = super().post(request, *args, **kwargs)
            tokens = response.data
            user = Usuario.objects.get(username=request.data['username'])



            access_token = tokens['access']
            refresh_token = tokens['refresh']
            
            res = Response()

            res.data = {"success" : True,
                        "rol" : user.rol,
                        "username" : user.username
                        }

            res.set_cookie(
                key= "access_token",
                value = access_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )

            res.set_cookie(
                key= "refresh_token",
                value = refresh_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )
            return res
        except:
            return Response({"success":False})
        
class CustomRefreshTokenView(TokenRefreshView):
    def post(self, request, *args, **kargs):

        try:
            refresh_token = request.COOKIES.get('refresh_token')

            request.data['refresh'] = refresh_token

            response = super().post(request, *args, **kargs)

            tokens = response.data
            access_token = tokens['access']

            res = Response()

            res.data = {"refreshed":True}
            res.set_cookie(
                key= "access_token",
                value = access_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )
            return res
        except:
            return Response({"refresh":False})
        
@api_view(["POST"])
def logout(request):
    try:
        res =Response()
        res.data = {"success":True}
        res.delete_cookie('access_token', path='/', samesite='None')
        res.delete_cookie('refresh_token', path='/', samesite='None')
        return res
    except:
        return Response({"success":False})
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def is_authenticated(request):
    return Response({'authenticated':True})
        
@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdmin, IsEmpresa])
def get_movimientos(request):
    user = request.user
    movimientos = Movimientos.objects.filter(creador = user)
    serializer = MovimientosSerializer(movimientos, many=True)
    return Response(serializer.data)



@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdmin])
def set_rol(request, id):
    new_rol = request.data.get('rol')

    if not new_rol:
        return Response({'error':'Debes indicar el rol que deseas asignar'})

    try:
        user = Usuario.objects.get(id = id)
    except:
        return Response({'error':'Usuario no encontrado'}, status=404)
    
    if new_rol not in dict(Usuario.ROLES):
        return Response({'error':'Rol no valido'}, status= 400)
    
    user.rol = new_rol
    user.save()

    return Response({
        'success': True,
        'message': f'Rol actualizado correctamente a {new_rol}.',
        'usuario': {
            'id': user.id,
            'username': user.username,
            'rol': user.rol
        }
    }, status=200)
        