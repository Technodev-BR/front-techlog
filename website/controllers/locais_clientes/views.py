from typing import Union
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from controllers.login.auth import administrador, administrador_or_supervisor, usuario_login_by_user_id
from controllers.login.authorized import locais_clientes_usuario
from controllers.iscas.models import IscaModel
from .forms import LocaisClienteForm
from .models import LocaisClienteModel

@login_required()
def buscar(request: HttpRequest):
    try:
        data = []
        usuario_logado = usuario_login_by_user_id(request.user.id)
        locais_clientes = locais_clientes_usuario(usuario_logado)
        for local_cliente in locais_clientes:
            newData = {
                'id':local_cliente.id,
                'local_id':local_cliente.local.id,
                'cliente_id':local_cliente.cliente.id,
                'data_criado':f'{local_cliente.data_criado}',
                'data_alterado':f'{local_cliente.data_alterado}',
                'ativo':local_cliente.ativo
            }
            data.append(newData)
            
        return JsonResponse({'data': data})

    except Exception as ex:
        print(ex)

@login_required
def buscar_by_Id(request: HttpRequest, id : int):
    try:
        data = []
        usuario_login = usuario_login_by_user_id(request.user.id)
        locais_clientes = locais_clientes_usuario(usuario_login)
        for local_cliente in locais_clientes:
            if(id == local_cliente.id):
                data = {
                    'id':local_cliente.id,
                    'local_id':local_cliente.local.id,
                    'cliente_id':local_cliente.cliente.id,
                    'data_criado':f'{local_cliente.data_criado}',
                    'data_alterado':f'{local_cliente.data_alterado}',
                    'ativo':local_cliente.ativo
                }
        
        return JsonResponse({'data': data})
    except Exception as ex:
        print(ex)

@login_required
def buscar_by_local_Id(request: HttpRequest, id : int):
    try:
        data = []
        usuario_login = usuario_login_by_user_id(request.user.id)
        locais_clientes = locais_clientes_usuario(usuario_login)
        for local_cliente in locais_clientes:
            if(id == local_cliente.local.id):
                newData = {
                    'id':local_cliente.id,
                    'local_id':local_cliente.local.id,
                    'cliente_id':local_cliente.cliente.id,
                    'cliente_nome':f'{local_cliente.cliente.nome_fantasia}',
                    'data_criado':f'{local_cliente.data_criado}',
                    'data_alterado':f'{local_cliente.data_alterado}',
                    'ativo':local_cliente.ativo
                }
                data.append(newData)
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
            
            form = LocaisClienteForm(request.POST or None)     
            if(form.is_valid()):
                form_new = form.save(commit=False)
                form_new.ativo = True
                resultado = form.save()    
            else:
                errors = {field: [error for error in form.errors[field]] for field in form.errors}
                return JsonResponse({'sucesso':False, 'errors':errors})
            
            return JsonResponse({'sucesso':True, 'mensagem':"Local cliente cadastrado com sucesso", "id":resultado.id})
        
    except IntegrityError as ex:
        print(ex)
        return JsonResponse({'sucesso':False, 'mensagem':"Local cliente ativo já existe"})
    
    except Exception as ex:
        print(ex)
             
    return redirect("locais:index")   

@login_required
def deletar(request: HttpRequest, id : int) -> Union[HttpResponse, HttpResponseRedirect]:
    local_cliente = get_object_or_404(LocaisClienteModel,id=id,ativo=True)
    try:
        if request.method == "POST":
            usuario_login = usuario_login_by_user_id(request.user.id)
            if not(administrador(usuario_login)):
                return JsonResponse({'sucesso':False, 'mensagem':"Apenas administradores podem excluir"})
            
            if(local_cliente and not IscaModel.objects.filter(local_cliente__id=local_cliente.id,ativo=True).exists()):
                local_cliente.ativo = False
                local_cliente.save()
            else:
                return JsonResponse({'sucesso':False, 'mensagem':"Existe iscas ativas com esse local cliente"})
            
            return JsonResponse({'sucesso':True, 'mensagem':"Local cliente removido com sucesso"})
    except Exception as ex:
        print(ex)

    return redirect("locais:index")   

@login_required
def deletar_by_list_Id(request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
    try:
        if request.method == "POST":
            usuario_login = usuario_login_by_user_id(request.user.id)
            if not(administrador(usuario_login)):
                return JsonResponse({'sucesso':False, 'mensagem':"Apenas administradores podem excluir"})
            
            clientes = request.POST.getlist('list_id') or None
            clientes_list_unica = clientes[0]
            list_clientes = clientes_list_unica.split(",")
            
            if(len(list_clientes) > 0 and list_clientes[0] != ""):
                for cliente_id in list_clientes:
                    local_cliente = get_object_or_404(LocaisClienteModel,id=int(cliente_id),ativo=True)
                    if(local_cliente and not IscaModel.objects.filter(local_cliente__id=local_cliente.id,ativo=True).exists()):
                        local_cliente.ativo = False
                        local_cliente.save()
                    else:
                        return JsonResponse({'sucesso':False, 'mensagem':"Existe iscas ativas com esse local cliente"})
                return JsonResponse({'sucesso':True, 'mensagem':"Local cliente removido com sucesso"})
            
            return JsonResponse({'sucesso':True, 'mensagem':"Nenhum local cliente para ser removido"})
    except Exception as ex:
        print(ex)
        
    return redirect("locais:index")   