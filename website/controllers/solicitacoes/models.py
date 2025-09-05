from django.db import models
from django.db.models import Q
from django.forms import ValidationError
from django.utils import timezone
from controllers.iscas.models import IscaModel
from controllers.rastreamentos.models import RastreamentoModel

class SolicitacoesModel(models.Model):
    
    CHECKIN_CHOICES = (
        ('Checkin Pendente', 'Checkin Pendente'), 
        ('Checkin Aprovado', 'Checkin Aprovado'), 
        ('Checkin Reprovado', 'Checkin Reprovado'), 
    ) 
    
    CHECKOUT_CHOICES = (
        ('Aguardando Checkin', 'Aguardando Checkin'), 
        ('Checkout Pendente', 'Checkout Pendente'), 
        ('Checkout Aprovado', 'Checkout Aprovado'), 
        ('Checkout Reprovado', 'Checkout Reprovado'),  
    ) 
    
    IMPLANTACAO_CHOICES = (
        ('Implantada', 'Implantada'), 
        ('Pendente', 'Pendente'), 
    )
    
    VIAGEM_CHOICES = (
        ('Iniciada', 'Iniciada'), 
        ('Pendente', 'Pendente'), 
    )
    
    RESULTADO_CHOICES = (
        ('Em Analise', 'Em Analise'), 
        ('Aprovado', 'Aprovado'), 
        ('Reprovado', 'Reprovado'), 
    )
    
    id = models.AutoField(editable=False, primary_key=True, unique=True)
    checkin = models.CharField(max_length=255, choices=CHECKIN_CHOICES, default="Checkin Pendente",blank=True)
    checkout = models.CharField(max_length=255, choices=CHECKOUT_CHOICES, default="Aguardando Checkin",blank=True)
    implantacao = models.CharField(max_length=255,choices=IMPLANTACAO_CHOICES,default="Pendente",blank=True)
    viagem = models.CharField(max_length=255,choices=VIAGEM_CHOICES,default="Pendente",blank=True)
    resultado = models.CharField(max_length=255,choices=RESULTADO_CHOICES,default="Em Analise",blank=True)
    isca = models.ForeignKey(IscaModel, on_delete=models.PROTECT,)
    data_criado = models.DateTimeField(auto_created=True, default=timezone.now,blank=True)
    data_alterado = models.DateTimeField(auto_created=True, default=timezone.now,blank=True)
    ativo = models.BooleanField(default=True) 
    
    def clean(self):
        if not self.isca.ativo == True:
            raise ValidationError('Isca removida escolha outra')
        
    def save(self, *args, **kwargs):
        self.data_alterado = timezone.now()
        
        if(self.ativo == False and SolicitacoesModel.objects.filter(id=self.id,ativo=True).exists()):
            if(RastreamentoModel.objects.filter(isca__id=self.isca.id,ativo=True,resultado="Em viagem").exists()):
                raise ValidationError('Finalize o rastreio com a isca antes de desativar')
            
        if(self.isca.modelo == "Fake" and self.ativo == True and not SolicitacoesModel.objects.filter(id=self.id,checkout="Checkout Pendente").exists()):
            self.checkin = "Checkin Aprovado"
            self.checkout = "Checkout Pendente"
            self.resultado = "Em Analise"
            self.isca.status = "Em checkout"
            
        self.isca.save()
            
        super().save(*args, **kwargs)
        
    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['isca'],
                condition=Q(ativo=True),
                name="isca_ativo_unico"
            )
        ]
         
    def __str__(self):
        return f'ID : {self.id} | NUMERO ISCA : {self.isca.numero_isca} | CHECKIN : {self.checkin} | CHECKOUT : {self.checkout} | RESULTADO : {self.resultado} | DATA CRIADO : {self.data_criado}'
