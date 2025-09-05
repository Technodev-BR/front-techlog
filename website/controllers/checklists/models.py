from django.forms import ValidationError
from django.utils import timezone
from django.db import models
from controllers.solicitacoes.models import SolicitacoesModel
from controllers.rastreamentos.models import RastreamentoModel

class ChecklistModel(models.Model):
    ETAPA_CHOICES = (   
        ('Checkin', 'Checkin'), 
        ('Checkout', 'Checkout'), 
    )
    
    RESULTADO_CHOICES = (   
        ('Aprovado', 'Aprovado'), 
        ('Reprovado', 'Reprovado'), 
    )

    id = models.AutoField(editable=False, primary_key=True, unique=True)
    bateria = models.CharField(max_length=50,blank=True,choices=RESULTADO_CHOICES)
    posicionamento = models.CharField(max_length=50,blank=True,choices=RESULTADO_CHOICES)
    descricao = models.CharField(max_length=255,blank=True)
    resultado = models.CharField(max_length=60,choices=RESULTADO_CHOICES)
    etapa = models.CharField(max_length=50,choices=ETAPA_CHOICES)
    usuario_responsavel = models.CharField(max_length=100,blank=True)
    solicitacao = models.ForeignKey(SolicitacoesModel, on_delete=models.PROTECT)
    data_realizado = models.DateTimeField(auto_created=True, default=timezone.now,blank=True)
    data_alterado = models.DateTimeField(auto_created=True, default=timezone.now,blank=True)
 
    def clean(self):
        if not self.solicitacao.ativo == True:
            raise ValidationError("solicitação foi removida crie uma nova") 
        
        if(self.etapa == "Checkin" and  ChecklistModel.objects.filter(etapa="Checkin",resultado="Aprovado",solicitacao=self.solicitacao).exists()):
            raise ValidationError("Checkin ja foi aprovado")
       
        if(self.etapa == "Checkout" and not SolicitacoesModel.objects.filter(checkin="Checkin Aprovado",checkout="Checkout Pendente",ativo=True).exists()):
            raise ValidationError("Para fazer um checkout é preciso que tenha um checkin aprovado")
        
        if ChecklistModel.objects.filter(etapa="Checkout",solicitacao=self.solicitacao).exists():
            raise ValidationError("Checkout ja foi realizado")

    def save(self, *args, **kwargs):
        self.data_alterado = timezone.now()
        
        if(self.resultado == "Aprovado" and self.etapa == "Checkin"):
            self.solicitacao.checkin = "Checkin Aprovado"
            self.solicitacao.isca.status = "Em checkout"
            self.solicitacao.checkout = "Checkout Pendente"
            
        if(self.resultado == "Aprovado" and self.etapa == "Checkout"):
            self.solicitacao.checkout = "Checkout Aprovado"
            self.solicitacao.isca.status = "Pendente iniciar SM"
            self.solicitacao.resultado = "Aprovado"
         
        if(self.resultado == "Reprovado" and self.etapa == "Checkin"):
            self.solicitacao.checkin = "Checkin Reprovado" 
            
            checkin_reprovados = ChecklistModel.objects.filter(etapa="Checkin",resultado="Reprovado",solicitacao=self.solicitacao)
        
            if(checkin_reprovados.count() >= 2):
                self.solicitacao.checkout = "Checkout Reprovado"
                self.solicitacao.resultado = "Reprovado"
                self.solicitacao.ativo = False
                
                if(self.solicitacao.isca.modelo != "Retornável"):
                    self.solicitacao.isca.status = "Reprovado"
                    self.solicitacao.isca.ativo = False
                else:
                    self.solicitacao.isca.status = "Almoxarifado"
                
                rastreamento = RastreamentoModel.objects.filter(ativo=True,isca__id=self.solicitacao.isca.id).first()
                if(rastreamento):
                    rastreamento.resultado = "Finalizada"
                    rastreamento.ativo = False
                    rastreamento.save()
                
        if (self.etapa == "Checkout" and self.resultado == "Reprovado"):
            self.solicitacao.checkout = "Checkout Reprovado"
            self.solicitacao.resultado = "Reprovado"
            self.solicitacao.ativo = False
            
            if(self.solicitacao.isca.modelo != "Retornável"):
                self.solicitacao.isca.status = "Reprovado"
                self.solicitacao.isca.ativo = False
            else:
                self.solicitacao.isca.status = "Almoxarifado"
            
        
        self.solicitacao.save()
        super().save(*args, **kwargs)
        
    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'ID : {self.id} | RESPONSAVEL : {self.usuario_responsavel} | ETAPA : {self.etapa} | RESULTADO : {self.resultado} | NUMERO ISCA : {self.solicitacao.isca.numero_isca} | NUMERO SOLICITACAO : {self.solicitacao.id} | DATA REALIZADO : {self.data_realizado}'
    