from django.db import models
from django.db.models import Q
from django.forms import ValidationError
from django.utils import timezone
from controllers.clientes.models import ClienteModel

class OperacaoModel(models.Model):
    id = models.AutoField(editable=False, primary_key=True, unique=True)
    nome = models.CharField(max_length=255,unique=False)
    cliente = models.ForeignKey(ClienteModel, on_delete=models.PROTECT)
    data_criado = models.DateTimeField(auto_created=True, default=timezone.now,blank=True)
    data_alterado = models.DateTimeField(auto_created=True, default=timezone.now,blank=True)
    ativo = models.BooleanField(default=True,blank=True)
    
    def clean(self):
        if self.cliente.ativo == False:
            raise ValidationError('Cliente removido escolha outro')
   
    def save(self, *args, **kwargs):
        self.data_alterado = timezone.now()
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['nome']
        constraints = [
            models.UniqueConstraint(
                fields=['nome','cliente'],
                condition=Q(ativo=True),
                name="nome_cliente_ativo_unico"
            )
        ]

    def __str__(self):
        return f'ID : {self.id} | NOME CLIENTE : {self.cliente.nome_fantasia} | NOME OPERACAO : {self.nome} | DATA CRIADO : {self.data_criado}'