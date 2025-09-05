from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from django.core.validators import RegexValidator
from django.forms import ValidationError

ROLES = {
    'ADMINISTRADOR': 'ADMINISTRADOR',
    'SUPERVISOR' : 'SUPERVISOR',
    'OPERADOR' :'OPERADOR',
}

class UsuarioModel(models.Model,):

    ROLES_CHOICES = (    
        ('ADMINISTRADOR','ADMINISTRADOR'),
        ('SUPERVISOR','SUPERVISOR'),
        ('OPERADOR','OPERADOR'),
    )

    id = models.AutoField(editable=False, primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    roles = models.CharField(max_length=13, choices=ROLES_CHOICES)
    foto = models.ImageField(upload_to='foto_usuario/', blank=True)
    email = models.EmailField(max_length=155,blank=True)
    recebe_email = models.BooleanField(default=True)  
    telefone_regex = RegexValidator(regex=r'^\d{9,15}$', message="Entre com telefone colocando apenas numeros: '999999999'. ")
    telefone = models.CharField(validators=[telefone_regex],unique=False, max_length=17, blank=True)
    data_criado = models.DateTimeField(auto_created=True, default=timezone.now,blank=True)
    data_alterado = models.DateTimeField(auto_created=True, default=timezone.now,blank=True)
    ativo = models.BooleanField(default=True)
      
    def save(self, *args, **kwargs):
        self.data_alterado = timezone.now()
        super().save(*args, **kwargs)
        
    class Meta:
        ordering = ['user']
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                condition=Q(ativo=True),
                name="user_ativo_unico"
            )
        ]

    def __str__(self):
        return f'ID : {self.id} | NOME : {self.user.username} | EMAIL : {self.email} | NIVEL ACESSO : {self.roles} | DATA CRIADO : {self.data_criado}'
    
