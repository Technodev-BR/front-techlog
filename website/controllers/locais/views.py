from typing import Union
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from controllers.login.auth import administrador, administrador_or_supervisor, usuario_login_by_user_id
from controllers.login.authorized import locais_usuario
from controllers.locais_clientes.models import LocaisClienteModel
from controllers.locais_clientes import views as locais_clientes 
from .models import LocalModel
from .forms import LocalForm

@login_required()
def index(request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:  
    context = {}
    usuario_logado = usuario_login_by_user_id(request.user.id)
    locais = locais_usuario(usuario_logado,True)
    context['locais_list'] = locais
    context['titulo_page'] = "Locais"
    context['nav_local'] = True
    return render(request, "pages/local.html", context=context)

@login_required()
def buscar(request: HttpRequest):
    try:
        data = []
        usuario_logado = usuario_login_by_user_id(request.user.id)
        locais = locais_usuario(usuario_logado,True)
        for local in locais:
            newData = {
                'id':local.id,
                'nome':f'{local.nome}',
                'cep':f'{local.cep}',
                'estado_uf':f'{local.estado_uf}',
                'cidade':f'{local.cidade}',
                'rua':f'{local.rua}',
                'data_criado':f'{local.data_criado}',
                'data_alterado':f'{local.data_alterado}',
                'ativo':local.ativo
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
        locais = locais_usuario(usuario_logado,False)
        for local in locais:
            newData = {
                'id':local.id,
                'nome':f'{local.nome}',
                'cep':f'{local.cep}',
                'estado_uf':f'{local.estado_uf}',
                'cidade':f'{local.cidade}',
                'rua':f'{local.rua}',
                'data_criado':f'{local.data_criado}',
                'data_alterado':f'{local.data_alterado}',
                'ativo':local.ativo
            }
            data.append(newData)
        return JsonResponse({'data': data})
    except Exception as ex:
        print(ex)

@login_required
def buscar_by_Id(request: HttpRequest, id : int):
    try:
        usuario_login = usuario_login_by_user_id(request.user.id)
        locais = locais_usuario(usuario_login,True)
        for local in locais:
            if(id == local.id):
                data = {
                    'id':local.id,
                    'nome':f'{local.nome}',
                    'cep':f'{local.cep}',
                    'estado_uf':f'{local.estado_uf}',
                    'cidade':f'{local.cidade}',
                    'rua':f'{local.rua}',
                    'data_criado':f'{local.data_criado}',
                    'data_alterado':f'{local.data_alterado}',
                    'ativo':local.ativo
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
            
            form = LocalForm(request.POST or None)     
            if(form.is_valid()):
                form_new = form.save(commit=False)
                form_new.ativo = True
                resultado = form.save()
                
                if(resultado.id):
                    clientes = request.POST.getlist('clientes_list') or None
                    clientes_list_unica = clientes[0]
                    list_clientes = clientes_list_unica.split(",")
                    
                    request.POST._mutable=True
                    request.POST["local"] = resultado.id
                    if(len(list_clientes) > 0 and list_clientes[0] != ""):
                        for cliente_id in list_clientes:  
                            request.POST["cliente"] = int(cliente_id)
                            locais_clientes.cadastrar(request)
                        return JsonResponse({'sucesso':True, 'mensagem':"Local cadastrado e clientes foram adicionados com sucesso", "id":resultado.id})
            else:
                errors = {field: [error for error in form.errors[field]] for field in form.errors}
                return JsonResponse({'sucesso':False, 'errors':errors})
            
            return JsonResponse({'sucesso':True, 'mensagem':"Local cadastrado com sucesso", 'id':resultado.id})

    except IntegrityError as ex:
        print(ex)
        return JsonResponse({'sucesso':False, 'mensagem':"Local ativo já existe"})
    
    except Exception as ex:
        print(ex)

    return redirect("locais:index")

@login_required
def atualizar(request: HttpRequest, id : int) -> Union[HttpResponse, HttpResponseRedirect]:
    try:
        if(request.method == 'POST'): 
            local = get_object_or_404(LocalModel,id=id,ativo=True)
            usuario_login = usuario_login_by_user_id(request.user.id)
            if not(administrador_or_supervisor(usuario_login)):
                return JsonResponse({'sucesso':False, 'mensagem':"Apenas administradores ou supervisores podem atualizar"})
            
            form = LocalForm(request.POST or None, instance=local)
            if(form.is_valid()):
                new_post = form.save(commit=False)
                new_post.ativo = True
                resultado = form.save()
                
                if(resultado.id):
                    clientes = request.POST.getlist('clientes_list') or None
                    clientes_list_unica = clientes[0]
                    list_clientes = clientes_list_unica.split(",")
                    
                    request.POST._mutable=True
                    request.POST["local"] = resultado.id
                    locais_clientes_existentes = LocaisClienteModel.objects.filter(local__id=resultado.id,ativo=True)
                 
                    if(len(list_clientes) > 0 and list_clientes[0] != ""):
                        for cliente_id in list_clientes:
                            if not(LocaisClienteModel.objects.filter(local__id=resultado.id,cliente__id=int(cliente_id),ativo=True).exists()):
                                request.POST["cliente"] = int(cliente_id)
                                locais_clientes.cadastrar(request)
                      
                    if(len(locais_clientes_existentes) > 0 and (len(list_clientes) == 0 or list_clientes[0] == "")):
                        for local_cliente in locais_clientes_existentes:  
                            locais_clientes.deletar(request,local_cliente.id)
                            
                    if(len(locais_clientes_existentes) > 0 and (len(list_clientes) > 0 and list_clientes[0] != "")):
                        for local_cliente in locais_clientes_existentes:
                            existe = False
                            for cliente_id in list_clientes: 
                                if(local_cliente.cliente.id == int(cliente_id)): 
                                    existe = True
                            if not(existe):
                                locais_clientes.deletar(request,local_cliente.id)

            else:
                errors = {field: [error for error in form.errors[field]] for field in form.errors}
                return JsonResponse({'sucesso':False, 'errors':errors})
            
            return JsonResponse({'sucesso':True, 'mensagem':"Local atualizado com sucesso", 'id':resultado.id})
        
    except IntegrityError as ex:
        print(ex)
        return JsonResponse({'sucesso':False, 'mensagem':"Local ativo já existe"})
    
    except Exception as ex:
        print(ex)
       
    return redirect("locais:index")  

@login_required
def deletar(request: HttpRequest, id : int) -> Union[HttpResponse, HttpResponseRedirect]:
    local = get_object_or_404(LocalModel,id=id,ativo=True)
    try:
        if request.method == "POST":
            usuario_login = usuario_login_by_user_id(request.user.id)
            if not(administrador(usuario_login)):
                return JsonResponse({'sucesso':False, 'mensagem':"Apenas administradores podem excluir"})
            
            if(local and not LocaisClienteModel.objects.filter(local__id=local.id, ativo=True).exists()):
                local.ativo = False
                local.save()
            else:
                return JsonResponse({'sucesso':False, 'mensagem':"Existe clientes ativos com esse local"})
            
            return JsonResponse({'sucesso':True, 'mensagem':"Local removido com sucesso"})    
    except Exception as ex:
        print(ex)
       
    return redirect("locais:index")  