from rest_framework import serializers
from .models import Usuario, Empresa, Empleado, Turno, TurnosAsignados, Movimientos

class UserRegistrationSerializer(serializers.Serializer):
    class Meta:
        model = Usuario



class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    class Meta:
        model = Usuario
        fields = ['id','username', 'email', 'rol', 'first_name', 'last_name', 'password', 'date_joined']

        def create(self, validated_data):
            user = Usuario(
                email =validated_data['email'],
                first_name = validated_data['first_name'],
                last_name = validated_data['last_name'],
                username = validated_data['username']
            )

            user.set_password(validated_data['password'])
            user.save()
            return user
        
        
class EmpresaSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)  

    class Meta:
        model = Empresa
        fields = ['id', 'usuario', 'nombre', 'nit', 'descripcion', 'direccion', 'logo']


class EmpleadoSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    empresa = EmpresaSerializer(read_only=True)

    class Meta:
        model = Empleado
        fields = ['id', 'usuario', 'empresa', 'cargo', 'fecha_ingreso', 
                  'num_identificacion', 'genero', 'edad', 'foto_perfil']


class TurnoSerializer(serializers.ModelSerializer):
    empresa = EmpresaSerializer(read_only=True)

    class Meta:
        model = Turno
        fields = ['id', 'empresa', 'nombre_turno', 'hora_inicio', 'hora_fin']


class TurnosAsignadosSerializer(serializers.ModelSerializer):
    empleado = EmpleadoSerializer(read_only=True)
    tipo_turno = TurnoSerializer(read_only=True)

    class Meta:
        model = TurnosAsignados
        fields = ['id', 'empleado', 'tipo_turno', 'fecha']

class MovimientosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimientos
        fields = '__all__'
