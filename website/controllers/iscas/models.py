from django.utils import timezone
from django.forms import ValidationError
from django.db import models
from django.db.models import Q
from controllers.fornecedores.models import FornecedorModel,COMUNICACAO_CHOICES 
from controllers.locais_clientes.models import LocaisClienteModel
from controllers.operacoes.models import OperacaoModel

MODELOS = [
    'Retornável',
    'Fake', 
    'Descartável',
]

class IscaModel(models.Model):
    
    MODELOS_CHOICES = (
        ('Retornável', 'Retornável'), 
        ('Fake', 'Fake'), 
        ('Descartável', 'Descartável')
    )

    STATUS_CHOICES = (
        ('Em checkin', 'Em checkin'), 
        ('Em checkout', 'Em checkout'), 
        ('Pendente iniciar SM', 'Pendente iniciar SM'), 
        ('Em rastreamento', 'Em rastreamento'), 
        ('Descartado', 'Descartado'), 
        ('Reprovado', 'Reprovado'), 
        ('Usado', 'Usado'), 
        ('Almoxarifado', 'Almoxarifado'), 
    )
    
    id = models.AutoField(editable=False, primary_key=True, unique=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default="Almoxarifado",blank=True) 
    foto = models.ImageField(upload_to='foto_isca/', blank=True)
    numero_isca = models.CharField(max_length=255, unique=False)
    local_cliente = models.ForeignKey(LocaisClienteModel, on_delete=models.PROTECT)
    comunicacao = models.CharField(max_length=55, choices=COMUNICACAO_CHOICES)
    usuario_cadastrante = models.CharField(max_length=255,blank=True) 
    modelo = models.CharField(max_length=255, choices=MODELOS_CHOICES)
    fornecedor = models.ForeignKey(FornecedorModel, on_delete=models.PROTECT)
    operacao = models.ForeignKey(OperacaoModel, on_delete=models.PROTECT)
    data_criado = models.DateTimeField(auto_created=True, default=timezone.now,blank=True)
    data_alterado = models.DateTimeField(auto_created=True, default=timezone.now,blank=True)
    ativo = models.BooleanField(default=True) 
    
    def save(self, *args, **kwargs):
        self.data_alterado = timezone.now()
        
        super().save(*args, **kwargs)
  
    class Meta:
        ordering = ['numero_isca']
        constraints = [
            models.UniqueConstraint(
                fields=['numero_isca','fornecedor'],
                condition=Q(ativo=True),
                name="numero_isca_fornecedor_ativo_unico"
            )
        ]

    def __str__(self):
        return f'ID : {self.id} | NUMERO ISCA : {self.numero_isca} | CLIENTE : {self.operacao.cliente.nome_fantasia} | OPERACAO : {self.operacao.nome} | FONERCEDOR : {self.fornecedor.nome} | DATA CRIADO : {self.data_criado}'