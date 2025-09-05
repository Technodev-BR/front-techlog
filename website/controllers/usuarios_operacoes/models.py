from django.db import models
from django.db.models import Q
from django.forms import ValidationError
from controllers.operacoes.models import OperacaoModel
from controllers.usuarios.models import UsuarioModel
from django.utils import timezone

class UsuariosOperacaoModel(models.Model):
    id = models.AutoField(editable=False, primary_key=True, unique=True)
    operacao = models.ForeignKey(OperacaoModel,on_delete=models.PROTECT)
    usuario = models.ForeignKey(UsuarioModel, on_delete=models.PROTECT)
    data_criado = models.DateTimeField(auto_created=True, default=timezone.now,blank=True)
    data_alterado = models.DateTimeField(auto_created=True, default=timezone.now,blank=True)
    ativo = models.BooleanField(default=True) 
    
    def clean(self):
        if self.usuario.ativo == False and not UsuariosOperacaoModel.objects.filter(id=self.id).exists():
            raise ValidationError('Usuario sem permissão escolha outro')
    
    def save(self, *args, **kwargs):
        self.data_alterado = timezone.now()
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['usuario']
        constraints = [
            models.UniqueConstraint(
                fields=['operacao','usuario'],
                condition=Q(ativo=True),
                name="operacao_usuario_ativo_unico"
            )
        ]

    def __str__(self):
        return f'ID : {self.id} | NOME : {self.usuario.user.username} | OPERACAO : {self.operacao.nome} | DATA CRIADO : {self.data_criado}'
