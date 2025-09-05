from django.core.mail import send_mail
from datetime import datetime
from controllers.iscas.models import IscaModel
from controllers.usuarios.models import UsuarioModel
from controllers.rastreamentos.models import RastreamentoModel
from controllers.login.authorized import iscas_usuario

def email_checklists_aprovacao(titulo : str,isca : IscaModel, usuario_logado : str):
    usuarios = UsuarioModel.objects.filter(ativo=True)
    lista_usuarios = []
    if(len(usuarios) > 0):
        for usuario in usuarios:
            iscas_user = iscas_usuario(usuario,True)
            for isca_user in iscas_user:
                if(isca_user.id == isca.id and usuario.recebe_email == True):
                    lista_usuarios.append(usuario.email)
    lista_usuarios.append(isca.fornecedor.email)
    if(isca.local_cliente.cliente.recebe_email == True):
        lista_usuarios.append(isca.local_cliente.cliente.email)
    lista_usuarios_unica = list(set(lista_usuarios))
    html_mensage = f"""
    <html>
        <body>
            <section>
                <p>Prezado(a) {isca.fornecedor.nome},</p><br/>
    
                <p>Solicitamos sua aprovação para a isca de número: <strong>{isca.numero_isca}</strong></p>
    
                <p>Mais Informações:</p>
                <ul>
                    <li>Cliente - <strong>{isca.local_cliente.cliente.razao_social}</strong></li>
                    <li>Operação - <strong>{isca.operacao.nome}</strong></li>
                    <li>Comunicação - <strong>{isca.comunicacao}</strong></li>
                    <li>Modelo - <strong>{isca.modelo}</strong></li>
                    <li>Usuario Solicitante - <strong>{usuario_logado}</strong></li>
                </ul>
                
                <br/><p>Para mais informações, por favor, consulte o sistema de gestão de iscas pelo link <a href='https://jclog.jcgestaoderiscos.com.br'>https//jclog.jcgestaoderiscos.com.br</p></a><br/>
 
                <p>Aguardamos sua análise e aprovação.</p>
                
            </section>
        </body>
    </html>
    """
    send_mail(titulo,message="",html_message=html_mensage,from_email="naoresponda@jcgestaoderiscos.com.br",recipient_list=lista_usuarios_unica,fail_silently=False)

def alerta_isca_reprovada(titulo : str, isca : IscaModel, usuario_logado : str):
    usuarios = UsuarioModel.objects.filter(ativo=True)
    lista_usuarios = []
    if(len(usuarios) > 0):
        for usuario in usuarios:
            iscas_user = iscas_usuario(usuario,True)
            for isca_user in iscas_user:
                if(isca_user.id == isca.id and usuario.recebe_email == True):
                    lista_usuarios.append(usuario.email)
    lista_usuarios.append(isca.fornecedor.email)
    if(isca.local_cliente.cliente.recebe_email == True):
        lista_usuarios.append(isca.local_cliente.cliente.email)
    lista_usuarios_unica = list(set(lista_usuarios))
    html_mensage = f"""
    <html>
        <body>
            <section>
                <p>Prezados(as),</p><br/>
    
                <p>Alertando a <span style="background:red;color:white;padding: 2px 5px;border-radius:4px;">reprovação</span> da isca de número: <strong>{isca.numero_isca}</strong></p>
    
                <p>Mais Informações:</p>
                <ul>
                    <li>Cliente - <strong>{isca.local_cliente.cliente.razao_social}</strong></li>
                    <li>Operação - <strong>{isca.operacao.nome}</strong></li>
                    <li>Comunicação - <strong>{isca.comunicacao}</strong></li>
                    <li>Modelo - <strong>{isca.modelo}</strong></li>
                    <li>Usuario responsável - <strong>{usuario_logado}</strong></li>
                </ul>
                
                <br/><p>Para mais informações, por favor, consulte o sistema de gestão de iscas pelo link <a href='https://jclog.jcgestaoderiscos.com.br'>https//jclog.jcgestaoderiscos.com.br</p></a><br/>
 
            </section>
        </body>
    </html>
    """
    send_mail(titulo,message="",html_message=html_mensage,from_email="naoresponda@jcgestaoderiscos.com.br",recipient_list=lista_usuarios_unica,fail_silently=False)

def alerta_inicio_viagem(titulo : str, sm : RastreamentoModel, usuario_logado : str):
    usuarios = UsuarioModel.objects.filter(ativo=True)
    lista_usuarios = []
    if(len(usuarios) > 0):
        for usuario in usuarios:
            iscas_user = iscas_usuario(usuario,True)
            for isca_user in iscas_user:
                if(isca_user.id == sm.isca.id and usuario.recebe_email == True):
                    lista_usuarios.append(usuario.email)
    if(sm.isca.local_cliente.cliente.recebe_email == True):
        lista_usuarios.append(sm.isca.local_cliente.cliente.email)
    lista_usuarios_unica = list(set(lista_usuarios))
    html_mensage = f"""
    <html>
        <body>
            <section>
                <p>Prezados(as),</p><br/>
    
                <p>Alertando a criação da viagem número: <strong>{sm.sm}</strong></p>
    
                <p>Mais Informações:</p>
                <ul>
                    <li>Numero SM - <strong>{sm.sm}</strong></li>
                    <li>Nota Fiscal - <strong>{sm.nota_fiscal}</strong></li>
                    <li>Manifesto - <strong>{sm.manifesto}</strong></li>
                    <li>Motorista - <strong>{sm.motorista}</strong></li>
                    <li>Valor SM - <strong>{sm.valor_sm}</strong></li>
                    <li>Rota da inserção - <strong>{sm.rota_insercao}</strong></li>
                    <li>Rota do maior valor - <strong>{sm.rota_maior_valor}</strong></li>
                    <li>placa - <strong>{sm.placa}</strong></li>
                    <li>resultado - <strong>{sm.resultado}</strong></li>
                    <li>Data da implantacao - <strong>{sm.data_implantacao.strftime("%d/%m/%Y %H:%M")}</strong></li>
                    <li>Data da saída - <strong>{sm.data_saida.strftime("%d/%m/%Y %H:%M")}</strong></li>
                    <li>Usuario responsável - <strong>{usuario_logado}</strong></li>
                </ul>
                
                <br/><p>Para mais informações, por favor, consulte o sistema de gestão de iscas pelo link <a href='https://jclog.jcgestaoderiscos.com.br'>https//jclog.jcgestaoderiscos.com.br</p></a><br/>
 
            </section>
        </body>
    </html>
    """
    send_mail(titulo,message="",html_message=html_mensage,from_email="naoresponda@jcgestaoderiscos.com.br",recipient_list=lista_usuarios_unica,fail_silently=False)


def alerta_fim_viagem(titulo : str, sm : RastreamentoModel, usuario_logado : str):
    usuarios = UsuarioModel.objects.filter(ativo=True)
    data_saida = None
    if(sm.data_saida):
        data_saida = sm.data_saida.strftime("%d/%m/%Y %H:%M")
    lista_usuarios = []
    if(len(usuarios) > 0):
        for usuario in usuarios:
            iscas_user = iscas_usuario(usuario,True)
            for isca_user in iscas_user:
                if(isca_user.id == sm.isca.id and usuario.recebe_email == True):
                    lista_usuarios.append(usuario.email)
    if(sm.isca.local_cliente.cliente.recebe_email == True):
        lista_usuarios.append(sm.isca.local_cliente.cliente.email)
    lista_usuarios_unica = list(set(lista_usuarios))
    html_mensage = f"""
    <html>
        <body>
            <section>
                <p>Prezados(as),</p><br/>
    
                <p>Alertando a <span style="background:red;color:white;padding: 2px 5px;border-radius:4px;">Finalização</span> da viagem número: <strong>{sm.sm}</strong></p>
    
                <p>Mais Informações:</p>
                <ul>
                    <li>Numero SM - <strong>{sm.sm}</strong></li>
                    <li>Nota Fiscal - <strong>{sm.nota_fiscal}</strong></li>
                    <li>Manifesto - <strong>{sm.manifesto}</strong></li>
                    <li>Motorista - <strong>{sm.motorista}</strong></li>
                    <li>Valor SM - <strong>{sm.valor_sm}</strong></li>
                    <li>Rota da inserção - <strong>{sm.rota_insercao}</strong></li>
                    <li>Rota do maior valor - <strong>{sm.rota_maior_valor}</strong></li>
                    <li>placa - <strong>{sm.placa}</strong></li>
                    <li>resultado - <strong>{sm.resultado}</strong></li>
                    <li>Data da implantacao - <strong>{sm.data_implantacao.strftime("%d/%m/%Y %H:%M")}</strong></li>
                    <li>Data da saída - <strong>{data_saida }</strong></li>
                    <li>Usuario responsável - <strong>{usuario_logado}</strong></li>
                </ul>
                
                <br/><p>Para mais informações, por favor, consulte o sistema de gestão de iscas pelo link <a href='https://jclog.jcgestaoderiscos.com.br'>https//jclog.jcgestaoderiscos.com.br</p></a><br/>
   
            </section>
        </body>
    </html>
    """
    send_mail(titulo,message="",html_message=html_mensage,from_email="naoresponda@jcgestaoderiscos.com.br",recipient_list=lista_usuarios_unica,fail_silently=False)


def alerta_nova_solicitacao(iscas : list[str] | None, usuario_logado : str ):
    ul_isca = "<ul>"
    if(len(iscas) > 0):
        for isca_id in iscas: 
            isca = IscaModel.objects.get(id=isca_id,ativo=True)
            li_isca = f"<li> Isca numero - {isca.numero_isca}</li>"   
            ul_isca = ul_isca + li_isca
    data = datetime.now()
    data_formatada = data.strftime("%d/%m/%Y %H:%M")
    ul_isca = ul_isca + f"</ul><p>Data criado: {data_formatada}</p><br/><br/>"
    html_mensage = f"""
    <html>
        <body>
            <section>
                <p>Prezados(as),</p><br/>
    
                <p>Foram criadas novas solicitações pelo usuario: <strong>{usuario_logado}</strong></p>
    
                {ul_isca}

                <p><strong>Atenciosamente</strong>,<br/><br/>Controle de Isca</p>  
            </section>
        </body>
    </html>
    """

    send_mail("CONTROLE DE ISCAS - NOVA SOLICITAÇÂO",message="",html_message=html_mensage,from_email="naoresponda@jcgestaoderiscos.com.br",recipient_list=["flavio.junior@jcgestaoderiscos.com.br"],fail_silently=False)