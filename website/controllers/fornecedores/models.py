from django.db import models
from django.core.validators import RegexValidator
from django.forms import ValidationError
from django.db.models import Q
from django.utils import timezone

COMUNICACAO = [
    'Radio Frequência', 
    'Hibrido',
    'GPRS',
]
COMUNICACAO_CHOICES = (
    ('Radio Frequência', 'Radio Frequência'), 
    ('Hibrido', 'Hibrido'), 
    ('GPRS', 'GPRS')
)

class FornecedorModel(models.Model):
    id = models.AutoField(editable=False, primary_key=True, unique=True)
    email = models.EmailField(max_length=155,blank=True)
    recebe_email = models.BooleanField(default=True)  
    telefone_regex = RegexValidator(regex=r'^\d{9,15}$', message="Entre com telefone colocando apenas numeros: '999999999'. ")
    telefone = models.CharField(validators=[telefone_regex], unique=False, max_length=17, blank=True)
    nome = models.CharField(max_length=255) 
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
                name="nome_fornecedores_ativo_unico"
            )
        ]

    def __str__(self):
        return f'ID : {self.id} | NOME : {self.nome} | DATA CRIADO : {self.data_criado}'
    