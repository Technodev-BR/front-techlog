from django.db import models
from django.core.validators import RegexValidator
from django.forms import ValidationError
from django.db.models import Q
from django.utils import timezone

class LocalModel(models.Model):
    id = models.AutoField(editable=False, primary_key=True, unique=True)
    nome = models.CharField(max_length=255)
    cep = models.CharField(max_length=8,blank=True)
    estado_uf = models.CharField(max_length=2,blank=True)
    cidade = models.CharField(max_length=150,blank=True)
    rua = models.CharField(max_length=255,blank=True)
    data_criado = models.DateTimeField(auto_created=True, default=timezone.now,blank=True)
    data_alterado = models.DateTimeField(auto_created=True, default=timezone.now,blank=True)
    ativo = models.BooleanField(default=True) 
    
    def save(self, *args, **kwargs):
        self.data_alterado = timezone.now()
        super().save(*args, **kwargs)
        
    class Meta:
        ordering = ['nome']
        constraints = [
            models.UniqueConstraint(
                fields=['nome'],
                condition=Q(ativo=True),
                name="nome_local_ativo_unico"
            )
        ]

    def __str__(self):
        return f'ID : {self.id} | NOME : {self.nome} | CEP : {self.cep} | DATA CRIADO : {self.data_criado}'
