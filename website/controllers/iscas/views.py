from typing import Union
import cv2
import base64
import numpy
from pyzbar.pyzbar import decode
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from controllers.login.auth import usuario_login_by_user_id
from controllers.login.authorized import iscas_usuario
from controllers.solicitacoes.models import SolicitacoesModel
from controllers.rastreamentos.models import RastreamentoModel
from .forms import IscaForm
from .models import IscaModel

@login_required()
def index(request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:  
    context = {}
    usuario_logado = usuario_login_by_user_id(request.user.id)
    iscas = iscas_usuario(usuario_logado,True)
    context['iscas_list'] = iscas
    context['titulo_page'] = "Inventario"
    context['nav_isca'] = True
    return render(request, "pages/inventario.html", context=context)

@login_required()
def buscar(request: HttpRequest):
    try:
        data = []
        usuario_logado = usuario_login_by_user_id(request.user.id)
        iscas = iscas_usuario(usuario_logado,True)
        for isca in iscas:
            newData = {
               'id':isca.id,
                'numero_isca':f'{isca.numero_isca}',
                'foto':f'{isca.foto}',
                'status':f'{isca.status}',
                'local_cliente_id':isca.local_cliente.id,
                'local_nome':f'{isca.local_cliente.local.nome}',
                'comunicacao':f'{isca.comunicacao}',
                'modelo':f'{isca.modelo}',
                'fornecedor_id':isca.fornecedor.id,
                'fornecedor_nome':f'{isca.fornecedor.nome}',
                'operacao_id':isca.operacao.id,
                'operacao_cliente_nome':f'{isca.operacao.cliente.nome_fantasia}',
                'operacao_cliente_razao_social':f'{isca.operacao.cliente.razao_social}',
                'operacao_nome':f'{isca.operacao.nome}',
                'usuario_cadastrante':f'{isca.usuario_cadastrante}',
                'data_criado':f'{isca.data_criado}',
                'data_alterado':f'{isca.data_alterado}',
                'ativo':isca.ativo
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
        iscas = iscas_usuario(usuario_logado,False)
        for isca in iscas:
            newData = {
                'id':isca.id,
                'numero_isca':f'{isca.numero_isca}',
                'foto':f'{isca.foto}',
                'status':f'{isca.status}',
                'local_cliente_id':isca.local_cliente.id,
                'local_nome':f'{isca.local_cliente.local.nome}',
                'comunicacao':f'{isca.comunicacao}',
                'modelo':f'{isca.modelo}',
                'fornecedor_id':isca.fornecedor.id,
                'fornecedor_nome':f'{isca.fornecedor.nome}',
                'operacao_id':isca.operacao.id,
                'operacao_cliente_nome':f'{isca.operacao.cliente.nome_fantasia}',
                'operacao_nome':f'{isca.operacao.nome}',
                'usuario_cadastrante':f'{isca.usuario_cadastrante}',
                'data_criado':f'{isca.data_criado}',
                'data_alterado':f'{isca.data_alterado}',
                'ativo':isca.ativo
            }
            data.append(newData)
        return JsonResponse({'data': data})
    except Exception as ex:
        print(ex)
        
@login_required
def buscar_by_Id(request: HttpRequest,id):
    try:
        data = []
        usuario_logado = usuario_login_by_user_id(request.user.id)
        iscas = iscas_usuario(usuario_logado,True)
        for isca in iscas:
            if(id == isca.id):
                data = {
                    'id':isca.id,
                    'numero_isca':f'{isca.numero_isca}',
                    'foto':f'{isca.foto}',
                    'status':f'{isca.status}',
                    'local_cliente_id':isca.local_cliente.id,
                    'local_nome':f'{isca.local_cliente.local.nome}',
                    'comunicacao':f'{isca.comunicacao}',
                    'modelo':f'{isca.modelo}',
                    'fornecedor_id':isca.fornecedor.id,
                    'fornecedor_nome':f'{isca.fornecedor.nome}',
                    'operacao_id':isca.operacao.id,
                    'operacao_cliente_nome':f'{isca.operacao.cliente.nome_fantasia}',
                    'operacao_nome':f'{isca.operacao.nome}',
                    'usuario_cadastrante':f'{isca.usuario_cadastrante}',
                    'data_criado':f'{isca.data_criado}',
                    'data_alterado':f'{isca.data_alterado}',
                    'ativo':isca.ativo
                }
        return JsonResponse({'data': data})
    except Exception as ex:
        print(ex)
 
@login_required
def cadastrar(request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
    try:
        if request.method == "POST":
            form = IscaForm(request.POST or None,request.FILES)     
            if(form.is_valid()):
                form_new = form.save(commit=False)
                form_new.ativo = True
                form_new.usuario_cadastrante = request.user
                resultado = form.save()
            else:
                errors = {field: [error for error in form.errors[field]] for field in form.errors}
                return JsonResponse({'sucesso':False, 'errors':errors})  
    
            return JsonResponse({'sucesso':True, 'mensagem':"Isca cadastrada com sucesso", "id":resultado.id})
        
    except IntegrityError as ex:
        print(ex)
        return JsonResponse({'sucesso':False, 'mensagem':"Isca com esse fornecedor ativa já existe"})
    except Exception as ex:
        print(ex)
             
    return redirect("iscas:index")

@login_required
def atualizar(request: HttpRequest, id : int) -> Union[HttpResponse, HttpResponseRedirect]:
    try:
        if(request.method == 'POST'):
            iscas = get_object_or_404(IscaModel,id=id,ativo=True)
            form = IscaForm(request.POST or None, instance=iscas)
            if(form.is_valid()):
                new_post = form.save(commit=False)
                new_post.ativo = True
                resultado = form.save()
            else:
                errors = {field: [error for error in form.errors[field]] for field in form.errors}
                return JsonResponse({'sucesso':False, 'errors':errors})  
            
            return JsonResponse({'sucesso':True, 'mensagem':"Isca atualizada com sucesso", "id":resultado.id})
        
    except IntegrityError as ex:
        print(ex)
        return JsonResponse({'sucesso':False, 'mensagem':"Isca com esse fornecedor ativa já existe"})
    
    except Exception as ex:
        print(ex)
             
    return redirect("iscas:index")

@login_required
def deletar(request: HttpRequest, id : int) -> Union[HttpResponse, HttpResponseRedirect]:
    try:
        if(request.method == 'POST'):
            isca = get_object_or_404(IscaModel,id=id,ativo=True)
            if(isca and not RastreamentoModel.objects.filter(isca__id=isca.id, ativo=True).exists() and not SolicitacoesModel.objects.filter(isca__id=isca.id,ativo=True).exists()):
                isca.ativo = False
                isca.status = "Descartado"
                isca.save()
            else:
                return JsonResponse({'sucesso':False, 'mensagem':"Existe rastreamentos ou solicitações ativos com essa isca"})
            
            return JsonResponse({'sucesso':True, 'mensagem':"Isca removida com sucesso"})    
    except Exception as ex:
        print(ex)
             
    return redirect("iscas:index")

@login_required
def leitor_qrcode(request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
    try:
        if(request.method == 'POST'):
            image_data = request.POST['image']
            
            format, image_string = image_data.split(';base64,')
            image_data = base64.b64decode(image_string)
            
            np_image = numpy.fromstring(image_data, numpy.uint8)
            image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
            
            decoded_objeto = decode(image)
            
            if(decoded_objeto):
                qrcode_data = decoded_objeto[0].data.decode('utf-8')
                return JsonResponse({'sucesso':True, 'data':qrcode_data})
            
            return JsonResponse({'sucesso':False, 'data':None})    
    except Exception as ex:
        print(ex)
             
    return redirect("iscas:index")