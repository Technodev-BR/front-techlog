from django.db import models
from django.db.models import Q
from django.forms import ValidationError
from django.utils import timezone
from controllers.iscas.models import IscaModel

class RastreamentoModel(models.Model):
    RESULTADO_CHOICES = (
        ('Implantada', 'Implantada'), 
        ('Em viagem', 'Em viagem'), 
        ('Finalizado', 'Finalizado'), 
    )

    id = models.AutoField(editable=False, primary_key=True, unique=True)
    sm = models.CharField(max_length=255,unique=False,blank=True)
    nota_fiscal = models.CharField(max_length=255,blank=True) 
    manifesto = models.CharField(max_length=255,blank=True) 
    volume = models.IntegerField(null=True,blank=True) 
    motorista = models.CharField(max_length=255,blank=True) 
    valor_sm = models.DecimalField(max_digits=17, decimal_places=2,null=True,blank=True) 
    rota_insercao = models.CharField(max_length=255,blank=True) 
    rota_maior_valor = models.CharField(max_length=255,blank=True) 
    placa = models.CharField(max_length=255,blank=True) 
    isca = models.ForeignKey(IscaModel, on_delete=models.PROTECT)
    resultado = models.CharField(max_length=255,choices=RESULTADO_CHOICES,default="Implantada",blank=True)
    data_implantacao = models.DateTimeField(auto_created=True, default=timezone.now,blank=True)
    data_saida = models.DateTimeField(null=True,blank=True)
    data_criado = models.DateTimeField(auto_created=True, default=timezone.now,blank=True)
    data_alterado = models.DateTimeField(auto_created=True, default=timezone.now,blank=True)
    ativo = models.BooleanField(default=True,blank=True) 
    
    def clean(self):
        if self.isca.ativo == False:
            raise ValidationError('Isca removido escolha outra')
        
    def save(self, *args, **kwargs):
        self.data_alterado = timezone.now()
        
        if self.ativo == False and RastreamentoModel.objects.filter(id=self.id,ativo=True).exists():
            self.isca.status = "Almoxarifado"
            self.isca.save()        
            
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['sm','isca'],
                condition=Q(ativo=True),
                name="sm_isca_ativo_unico"
            )
        ]

    def __str__(self):
        return f'ID : {self.id} | SM : {self.sm} | PLACA : {self.placa} | NUMERO ISCA : {self.isca.numero_isca} | NOTA FISCAL : {self.nota_fiscal} | DATA CRIADO : {self.data_criado}'

class RastreamentoAnexoModel(models.Model):
    id = models.AutoField(editable=False, primary_key=True, unique=True)
    foto = models.ImageField(upload_to='foto_rastreio/', blank=True)
    rastreamento = models.ForeignKey(RastreamentoModel, on_delete=models.PROTECT)
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return f'ID : {self.id} FOTO : {self.foto}'
