from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings

class Usuario(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('empresa', 'Empresa'),
        ('empleado', 'Empleado')
    )

    rol = models.CharField(max_length=20, choices=ROLES, default='Empresa')

class Empresa(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='empresa')
    nombre = models.CharField(max_length=100)
    nit = models.CharField(max_length=20, unique=True)
    descripcion = models.TextField(max_length=1000)
    direccion = models.CharField(max_length=100)
    logo = models.URLField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.nombre
    

class Empleado(models.Model):
    GENEROS = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro')
    )
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='empleado')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='empleados')
    cargo = models.CharField(max_length=100)
    fecha_ingreso = models.DateField()
    num_identificacion = models.IntegerField()
    genero = models.CharField(max_length=2, choices=GENEROS, default='Otro')
    edad = models.IntegerField()
    foto_perfil = models.URLField(max_length=300, blank=True, null=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.cargo}"
    

class Turno(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="tipos_turno")
    nombre_turno = models.CharField(max_length=50)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

class TurnosAsignados(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='turnos_asignados')
    tipo_turno = models.ForeignKey(Turno, on_delete=models.CASCADE, related_name= 'asignaciones')
    fecha = models.DateField()

class Movimientos(models.Model):
    TIPO_MOVIMIENTO = (
        ("I", "Ingreso"),
        ("R", "Retiro")
    )
    creador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="movimiento" ,null=True,  blank=True)
    num_identificacion = models.IntegerField()
    nombre = models.CharField(max_length=100)
    Tipo_movimiento = models.CharField(max_length=2, choices=TIPO_MOVIMIENTO, default=
    "Ingreso")


