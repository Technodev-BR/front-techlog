from typing import Union
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from controllers.login.auth import administrador, administrador_or_supervisor, usuario_login_by_user_id
from controllers.login.authorized import clientes_usuario
from controllers.locais_clientes.models import LocaisClienteModel
from controllers.iscas.models import IscaModel
from controllers.operacoes.models import OperacaoModel
from controllers.operacoes import views as Operacoes
from .models import ClienteModel
from .forms import ClienteForm

@login_required()
def index(request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
    context = {}
    usuario_logado = usuario_login_by_user_id(request.user.id)
    if not(administrador_or_supervisor(usuario_logado)):
        return redirect("home")  
    clientes = clientes_usuario(usuario_logado,True)
    context['clientes_list'] = clientes
    context['titulo_page'] = "Clientes"
    context['nav_cliente'] = True
    return render(request, "pages/cliente.html", context)

@login_required()
def buscar(request: HttpRequest):
    try:
        data = []
        usuario_logado = usuario_login_by_user_id(request.user.id)
        clientes = clientes_usuario(usuario_logado,True)
        for cliente in clientes:
            newData = {
                'id':cliente.id,
                'nome_fantasia':f'{cliente.nome_fantasia}',
                'razao_social':f'{cliente.razao_social}',
                'cnpj':f'{cliente.cnpj}',
                'uf':f'{cliente.uf}',
                'cidade':f'{cliente.cidade}',
                'bairro':f'{cliente.bairro}',
                'rua':f'{cliente.rua}',
                'email':f'{cliente.email}',
                'recebe_email':cliente.recebe_email,
                'data_criado':f'{cliente.data_criado}',
                'data_alterado':f'{cliente.data_alterado}',
                'ativo':cliente.ativo
            }
            data.append(newData)
        return JsonResponse({'data': data})
    except Exception as ex:
        print(ex)
        
     
@login_required()
def buscar_removidos(request: HttpRequest):
    try:
        data = []
        usuario_logado = usuario_login_by_user_id(request.user.id)
        clientes = clientes_usuario(usuario_logado,False)
        for cliente in clientes:
            newData = {
                'id':cliente.id,
                'nome_fantasia':f'{cliente.nome_fantasia}',
                'razao_social':f'{cliente.razao_social}',
                'cnpj':f'{cliente.cnpj}',
                'uf':f'{cliente.uf}',
                'cidade':f'{cliente.cidade}',
                'bairro':f'{cliente.bairro}',
                'rua':f'{cliente.rua}',
                'email':f'{cliente.email}',
                'recebe_email':cliente.recebe_email,
                'data_criado':f'{cliente.data_criado}',
                'data_alterado':f'{cliente.data_alterado}',
                'ativo':cliente.ativo
            }
            data.append(newData)
        return JsonResponse({'data': data})
    except Exception as ex:
        print(ex)

@login_required
def buscar_by_Id(request: HttpRequest, id : int):
    try:
        usuario_login = usuario_login_by_user_id(request.user.id)
        clientes = clientes_usuario(usuario_login,True)
        for cliente in clientes:
            if(id == cliente.id):
                data = {
                    'id':cliente.id,
                    'nome_fantasia':f'{cliente.nome_fantasia}',
                    'razao_social':f'{cliente.razao_social}',
                    'cnpj':f'{cliente.cnpj}',
                    'uf':f'{cliente.uf}',
                    'cidade':f'{cliente.cidade}',
                    'bairro':f'{cliente.bairro}',
                    'rua':f'{cliente.rua}',
                    'email':f'{cliente.email}',
                    'recebe_email':cliente.recebe_email,
                    'data_criado':f'{cliente.data_criado}',
                    'data_alterado':f'{cliente.data_alterado}',
                    'ativo':cliente.ativo
                }
        return JsonResponse({'data': data})
    except Exception as ex:
        print(ex)

@login_required
def cadastrar(request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
    try:
        if request.method == "POST":
            usuario_login = usuario_login_by_user_id(request.user.id)
            if not(administrador_or_supervisor(usuario_login)):
                return JsonResponse({'sucesso':False, 'mensagem':"Apenas administradores ou supervisores podem cadastrar"})
            
            form = ClienteForm(request.POST or None)     
            if(form.is_valid()):
                new_post = form.save(commit=False)
                new_post.ativo = True
                resultado = form.save()
                return JsonResponse({'sucesso':True, 'mensagem':"Cliente cadastrada com sucesso", "id":resultado.id})  
            else:
                errors = {field: [error for error in form.errors[field]] for field in form.errors}
                return JsonResponse({'sucesso':False, 'errors':errors})
    
    except IntegrityError as ex:
        return JsonResponse({'sucesso':False, 'mensagem':"Cliente ativo já existe"})
    except Exception as ex:
        print(ex)
    return redirect("clientes:index")

@login_required
def atualizar(request: HttpRequest, id : int) -> Union[HttpResponse, HttpResponseRedirect]:
    try:
        if(request.method == 'POST'):
            usuario_login = usuario_login_by_user_id(request.user.id)
            if not(administrador_or_supervisor(usuario_login)):
                return JsonResponse({'sucesso':False, 'mensagem':"Apenas administradores ou supervisores podem atualizar"})
                        
            cliente = get_object_or_404(ClienteModel,id=id,ativo=True)
            form = ClienteForm(request.POST or None, instance=cliente)
            if(form.is_valid()):
                new_post = form.save(commit=False)
                new_post.ativo = True
                resultado = form.save()
                return JsonResponse({'sucesso':True, 'mensagem':"Cliente atualizado com sucesso", "id":resultado.id})  
            else:
                errors = {field: [error for error in form.errors[field]] for field in form.errors}
                return JsonResponse({'sucesso':False, 'errors':errors})
    
    except IntegrityError as ex:
        return JsonResponse({'sucesso':False, 'mensagem':"Cliente ativo já existe"})
    except Exception as ex:
        print(ex)
             
    return redirect("clientes:index")

@login_required
def deletar(request: HttpRequest, id : int) -> Union[HttpResponse, HttpResponseRedirect]:
    cliente = get_object_or_404(ClienteModel,id=id,ativo=True)
    try:
        if(request.method == 'POST'):
            usuario_login = usuario_login_by_user_id(request.user.id)
            if not(administrador(usuario_login)):
                return JsonResponse({'sucesso':False, 'mensagem':"Apenas administradores podem excluir"})
            
            if(cliente and not LocaisClienteModel.objects.filter(cliente__id=cliente.id, ativo=True).exists() and not IscaModel.objects.filter(operacao__cliente__id=cliente.id, ativo=True).exists()):
                operacoes = OperacaoModel.objects.filter(cliente__id=cliente.id,ativo=True)      
                for operacao in operacoes:
                    Operacoes.deletar(request=request,id=operacao.id)
                cliente.ativo = False
                cliente.save()
            else:
                return JsonResponse({'sucesso':False, 'mensagem':"Existe Iscas ou locais ativos com esse cliente"})
                
            return JsonResponse({'sucesso':True, 'mensagem':"cliente removida com sucesso"})    
    except Exception as ex:
        print(ex)
       
    return redirect("clientes:index") 