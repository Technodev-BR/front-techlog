from django.db import models
from django.forms import ValidationError
from django.db.models import Q
from django.utils import timezone
from controllers.clientes.models import ClienteModel
from controllers.locais.models import LocalModel
    
class LocaisClienteModel(models.Model):
    id = models.AutoField(editable=False, primary_key=True, unique=True)
    local = models.ForeignKey(LocalModel, on_delete=models.PROTECT,unique=False)
    cliente = models.ForeignKey(ClienteModel, on_delete=models.PROTECT)
    data_criado = models.DateTimeField(auto_created=True, default=timezone.now,blank=True)
    data_alterado = models.DateTimeField(auto_created=True, default=timezone.now,blank=True)
    ativo = models.BooleanField(default=True) 
    
    def clean(self):
        if self.local.ativo == False:
            raise ValidationError('Local removido escolha outro')
        
        if self.cliente.ativo == False:
            raise ValidationError('Cliente removido escolha outro')
        
    def save(self, *args, **kwargs):
        self.data_alterado = timezone.now()
        
        super().save(*args, **kwargs)
        
    class Meta:
        ordering = ['local']
        constraints = [
            models.UniqueConstraint(
                fields=['local','cliente'],
                condition=Q(ativo=True),
                name="local_cliente_ativo_unico"
            )
        ]

    def __str__(self):
        return f'ID : {self.id} | LOCAL : {self.local.nome} | CLIENTE : {self.cliente.nome_fantasia} | DATA CRIADO : {self.data_criado}'