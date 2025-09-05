from django.db import models
from django.db.models import Q
from django.core.validators import RegexValidator
from django.utils import timezone

class ClienteModel(models.Model):
    id = models.AutoField(editable=False, primary_key=True, unique=True)
    nome_fantasia = models.CharField(max_length=155)
    razao_social = models.CharField(max_length=155,unique=False)
    cnpj = models.CharField(max_length=25)
    telefone_regex = RegexValidator(regex=r'^\d{9,15}$', message="Entre com telefone colocando apenas numeros: '999999999'. ")
    telefone = models.CharField(validators=[telefone_regex], unique=False, max_length=17, blank=True)
    cep = models.CharField(max_length=8,blank=True)
    uf = models.CharField(max_length=2,blank=True)
    cidade = models.CharField(max_length=100,blank=True)
    bairro = models.CharField(max_length=100,blank=True)
    rua = models.CharField(max_length=100,blank=True)
    email = models.EmailField(max_length=155,blank=True)
    recebe_email = models.BooleanField(default=True)  
    data_criado = models.DateTimeField(auto_created=True,default=timezone.now,blank=True)
    data_alterado = models.DateTimeField(auto_created=True,default=timezone.now,blank=True)
    ativo = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        self.data_alterado = timezone.now()
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['nome_fantasia']
        constraints = [
            models.UniqueConstraint(
                fields=['nome_fantasia','razao_social','cnpj'],
                condition=Q(ativo=True),
                name="nome_fantasia_razao_social_cnpj_ativo_unico"
            )
        ]

    def __str__(self):
        return f'ID : {self.id} | NOME : {self.nome_fantasia} | DATA CRIADO : {self.data_criado} | DATA ALTERADA : {self.data_alterado} | ATIVO : {self.ativo}'
