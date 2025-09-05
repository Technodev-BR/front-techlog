from controllers.checklists.models import ChecklistModel
from controllers.clientes.models import ClienteModel
from controllers.iscas.models import IscaModel
from controllers.locais.models import LocalModel
from controllers.locais_clientes.models import LocaisClienteModel
from controllers.rastreamentos.models import RastreamentoModel
from controllers.solicitacoes.models import SolicitacoesModel
from controllers.operacoes.models import OperacaoModel
from controllers.usuarios_operacoes.models import UsuariosOperacaoModel
from controllers.usuarios.models import UsuarioModel,ROLES

def clientes_usuario(usuario : UsuarioModel, ativo : bool):
    try:
        clientes = ClienteModel.objects.none()
        
        if not(usuario):
            return clientes
        
        if(usuario.roles == ROLES['OPERADOR']):
            operacoes_usuario = UsuariosOperacaoModel.objects.filter(usuario__id=usuario.id,ativo=True)   
            
            clientes_id = []
            if(operacoes_usuario):
                for operacao_usuario in operacoes_usuario:
                    clientes_id.append(operacao_usuario.operacao.cliente.id)
                
            clientes_id_formatado = list(dict.fromkeys(clientes_id))
            clientes = ClienteModel.objects.filter(id__in=clientes_id_formatado,ativo=ativo)
            return clientes 
            
        if(usuario.roles == ROLES['ADMINISTRADOR'] or usuario.roles == ROLES['SUPERVISOR']):
            clientes = ClienteModel.objects.filter(ativo=ativo)
            return clientes
        
    except Exception as ex:
        print(ex)

def locais_usuario(usuario : UsuarioModel, ativo : bool):
    try:
        locais = LocalModel.objects.none()
        
        if not(usuario):
            return locais
        
        if(usuario.roles == ROLES['OPERADOR']):
            operacoes_usuario = UsuariosOperacaoModel.objects.filter(usuario__id=usuario.id, ativo=True)   
            
            clientes_id = []
            if(operacoes_usuario):
                for operacao_usuario in operacoes_usuario:
                    clientes_id.append(operacao_usuario.operacao.cliente.id)
                
            clientes_id_formatado = list(dict.fromkeys(clientes_id))
            locais = LocalModel.objects.filter(id__in=LocaisClienteModel.objects.filter(cliente__id__in=clientes_id_formatado,ativo=ativo).values("id"),ativo=ativo)
            return locais 
            
        if(usuario.roles == ROLES['ADMINISTRADOR'] or usuario.roles == ROLES['SUPERVISOR']):
            locais = LocalModel.objects.filter(ativo=ativo)
            return locais
        
    except Exception as ex:
        print(ex) 
    
def locais_clientes_usuario(usuario : UsuarioModel):
    try:
        locais_clientes = LocaisClienteModel.objects.none()
        
        if not(usuario):
            return locais_clientes
        
        if(usuario.roles == ROLES['OPERADOR']):
            operacoes_usuario = UsuariosOperacaoModel.objects.filter(usuario__id=usuario.id,ativo=True)   
            
            clientes_id = []
            if(operacoes_usuario):
                for operacao_usuario in operacoes_usuario:
                    clientes_id.append(operacao_usuario.operacao.cliente.id)
                
            clientes_id_formatado = list(dict.fromkeys(clientes_id))
            locais_clientes = LocaisClienteModel.objects.filter(cliente__id__in=clientes_id_formatado,ativo=True)
            return locais_clientes 
            
        if(usuario.roles == ROLES['ADMINISTRADOR'] or usuario.roles == ROLES['SUPERVISOR']):
            locais_clientes = LocaisClienteModel.objects.filter(ativo=True)
            return locais_clientes
        
    except Exception as ex:
        print(ex)

def operacoes_usuario(usuario : UsuarioModel):
    try:
        operacoes = OperacaoModel.objects.none()
        
        if not(usuario):
            return operacoes
        
        if(usuario.roles == ROLES['OPERADOR']):
            operacoes_usuario = UsuariosOperacaoModel.objects.filter(usuario__id=usuario.id,operacao__cliente__ativo=True,ativo=True)   
            
            operacoes_id = []
            if(operacoes_usuario):
                for operacao_usuario in operacoes_usuario:
                    operacoes_id.append(operacao_usuario.operacao.id)
                
            operacoes = OperacaoModel.objects.filter(id__in=operacoes_id,ativo=True)
            return operacoes 
            
        if(usuario.roles == ROLES['ADMINISTRADOR'] or usuario.roles == ROLES['SUPERVISOR']):
            operacoes = OperacaoModel.objects.filter(ativo=True)
            return operacoes
        
    except Exception as ex:
        print(ex)

def iscas_usuario(usuario : UsuarioModel, ativo : bool):
    try:
        
        iscas = IscaModel.objects.none()
          
        if not(usuario):
            return iscas
        
        if(usuario.roles == ROLES['OPERADOR']):
            operacoes_usuario = UsuariosOperacaoModel.objects.filter(usuario__id=usuario.id,ativo=True)   
            
            operacoes_id = []
            if(operacoes_usuario):
                for operacao_usuario in operacoes_usuario:
                    operacoes_id.append(operacao_usuario.operacao.id)
                
            iscas = IscaModel.objects.filter(operacao__id__in=operacoes_id,ativo=ativo)
            return iscas 
            
        if(usuario.roles == ROLES['ADMINISTRADOR'] or usuario.roles == ROLES['SUPERVISOR']):
            iscas = IscaModel.objects.filter(ativo=ativo)
            return iscas
        
    except Exception as ex:
        print(ex)

def solicitacoes_usuario(usuario : UsuarioModel, ativo : bool):
    try:
        solicitacoes = SolicitacoesModel.objects.none()
        
        if not(usuario):
            return solicitacoes
        
        if(usuario.roles == ROLES['OPERADOR']):
            operacoes_usuario = UsuariosOperacaoModel.objects.filter(usuario__id=usuario.id,ativo=True)   
            
            operacoes_id = []
            if(operacoes_usuario):
                for operacao_usuario in operacoes_usuario:
                    operacoes_id.append(operacao_usuario.operacao.id)
                
            solicitacoes = SolicitacoesModel.objects.filter(isca__operacao__id__in=operacoes_id,ativo=ativo)
            return solicitacoes 
            
        if(usuario.roles == ROLES['ADMINISTRADOR'] or usuario.roles == ROLES['SUPERVISOR']):
            solicitacoes = SolicitacoesModel.objects.filter(ativo=ativo)
            return solicitacoes
        
    except Exception as ex:
        print(ex)

def checklists_usuario(usuario : UsuarioModel):
    try:
        checklists = ChecklistModel.objects.none()
        
        if not(usuario):
            return checklists
        
        if(usuario.roles == ROLES['OPERADOR']):
            operacoes_usuario = UsuariosOperacaoModel.objects.filter(usuario__id=usuario.id,operacao__cliente__ativo=True,ativo=True)   
            
            operacoes_id = []
            if(operacoes_usuario):
                for operacao_usuario in operacoes_usuario:
                    operacoes_id.append(operacao_usuario.operacao.id)
                
            checklists = ChecklistModel.objects.filter(solicitacao__isca__operacao__id__in=operacoes_id,ativo=True)
            return checklists 
            
        if(usuario.roles == ROLES['ADMINISTRADOR'] or usuario.roles == ROLES['SUPERVISOR']):
            checklists = ChecklistModel.objects.filter(ativo=True)
            return checklists
        
    except Exception as ex:
        print(ex)

def rastreamentos_usuario(usuario : UsuarioModel, ativo : bool):
    try:
        rastreamentos = RastreamentoModel.objects.none()
        
        if not(usuario):
            return rastreamentos
        
        if(usuario.roles == ROLES['OPERADOR']):
            operacoes_usuario = UsuariosOperacaoModel.objects.filter(usuario__id=usuario.id,ativo=True)   
            
            operacoes_id = []
            if(operacoes_usuario):  
                for operacao_usuario in operacoes_usuario:
                    operacoes_id.append(operacao_usuario.operacao.id)
                
            rastreamentos = RastreamentoModel.objects.filter(isca__operacao__id__in=operacoes_id,ativo=ativo)
            return rastreamentos 
            
        if(usuario.roles == ROLES['ADMINISTRADOR'] or usuario.roles == ROLES['SUPERVISOR']):
            rastreamentos = RastreamentoModel.objects.filter(ativo=ativo)
            return rastreamentos
        
    except Exception as ex:
        print(ex)