from django.contrib.auth import login
from django.contrib.auth import authenticate, login as auth_login
from django.db.models import Count, F
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from .forms import RegisterForm, ProjetoForm, AnotacaoForm, IdeiaForm, TarefaForm
from .models import Projeto, Convite, Tarefa, Anotacao, Ideia, Notificacao
from django.contrib.auth.models import User

# ------------------------------------- /registration/ ------------------------------------------
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Credenciais inválidas. Tente novamente.')
            return redirect('user_login')

    return render(request, 'registration/login.html')
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            login(request, user)

            return redirect('index')
    else:
        form = RegisterForm()

    return render(request, 'registration/registro.html', {'form': form})

@login_required
def index(request):

    responsavel = Projeto.objects.filter(responsavel=request.user)

    projetos_participando = Projeto.objects.filter(
        convite__convidado=request.user, convite__status='aceito'
    )

    projetos = responsavel | projetos_participando

    return render(request, 'index.html', {'projetos': projetos})

# --------------------------------------------------------------------------------------

@login_required
def detalhes_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    ideias = Ideia.objects.filter(projeto=projeto)
    tarefas = Tarefa.objects.filter(projeto=projeto)
    anotacoes = Anotacao.objects.filter(projeto=projeto)


    usuarios = User.objects.exclude(id=request.user.id)


    convites_pendentes = Convite.objects.filter(projeto=projeto, status='pendente')

    usuarios_no_projeto = [convite.convidado for convite in convites_pendentes if convite.status == 'aceito']

    if 'buscar' in request.GET:
        termo = request.GET.get('buscar')
        if termo:
            usuarios = usuarios.filter(username__icontains=termo)

    if request.method == 'POST':
        convidado_id = request.POST.get('convidado_id')
        convidado = get_object_or_404(User, id=convidado_id)

        if not Convite.objects.filter(projeto=projeto, convidado=convidado).exists():
            convite = Convite.objects.create(
                projeto=projeto,
                convidado=convidado,
                enviado_por=request.user,
                status='pendente'
            )

            mensagem = f"Você foi convidado para o projeto '{projeto.nome}'."
            link = f"/detalhes_projeto/{projeto.id}/"
            Notificacao.objects.create(
                usuario=convidado,
                mensagem=mensagem,
                link=link
            )

            messages.success(request, f"Convite enviado para {convidado.username}!")
        else:
            messages.warning(request, f"{convidado.username} já foi convidado para este projeto.")

        return redirect('detalhes_projeto', projeto_id=projeto.id)

    return render(request, 'detalhes_projeto.html', {
        'projeto': projeto,
        'ideias': ideias,
        'tarefas': tarefas,
        'anotacoes': anotacoes,
        'usuarios': usuarios,
        'convites_pendentes': convites_pendentes,
        'usuarios_no_projeto': usuarios_no_projeto,
    })

@login_required
def marcar_como_lida(request, notificacao_id):
    notificacao = get_object_or_404(Notificacao, id=notificacao_id)
    notificacao.delete()
    messages.success(request, "Notificação marcada como lida e removida com sucesso.")
    return redirect('notificacoes')

@login_required
def criar_projeto(request):
    if request.method == 'POST':
        form = ProjetoForm(request.POST)
        if form.is_valid():
            projeto = form.save(commit=False)
            projeto.responsavel = request.user
            projeto.save()
            return redirect('index')
    else:
        form = ProjetoForm()

    return render(request, 'criar_projeto.html', {'form': form})

@login_required
def adicionar_tarefa(request, projeto_id):
    projeto = Projeto.objects.get(id=projeto_id)

    if request.method == 'POST':
        form = TarefaForm(request.POST)
        if form.is_valid():
            tarefa = form.save(commit=False)
            tarefa.projeto = projeto
            tarefa.criado_por = request.user
            tarefa.save()
            return redirect('detalhes_projeto', projeto_id=projeto.id)
    else:
        form = TarefaForm()

    return render(request, 'adicionar_tarefa.html', {'form': form, 'projeto': projeto})

def adicionar_nota(request, projeto_id):
    projeto = Projeto.objects.get(id=projeto_id)

    if request.method == 'POST':
        form = AnotacaoForm(request.POST)
        if form.is_valid():
            nota = form.save(commit=False)
            nota.projeto = projeto
            nota.criado_por = request.user
            nota.save()
            return redirect('detalhes_projeto', projeto_id=projeto.id)
    else:
        form = AnotacaoForm()

    return render(request, 'adicionar_nota.html', {'form': form, 'projeto': projeto})

def adicionar_ideia(request, projeto_id):
    projeto = Projeto.objects.get(id=projeto_id)

    if request.method == 'POST':
        form = IdeiaForm(request.POST)
        if form.is_valid():
            ideia = form.save(commit=False)
            ideia.projeto = projeto
            ideia.sugerido_por = request.user
            ideia.save()
            return redirect('detalhes_projeto', projeto_id=projeto.id)
    else:
        form = IdeiaForm()

    return render(request, 'adicionar_ideia.html', {'form': form, 'projeto': projeto})


@login_required
def notificacoes(request):
    notificacoes = Notificacao.objects.filter(usuario=request.user).order_by('-data_criacao')
    return render(request, 'notificacoes.html', {'notificacoes': notificacoes})

@login_required
def excluir_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)

    if projeto.responsavel == request.user:
        projeto.delete()
        return redirect('index')
    else:

        return redirect('acesso_negado')


#------------------------------------/DadosProjetos/-------------------------------------------------------------
from django.db.models import Count, Q

@login_required
def relatorios(request, projeto_id):
    # Buscar o projeto correspondente
    projeto = get_object_or_404(Projeto, id=projeto_id)

    # Total de atividades relacionadas ao projeto
    total_tarefas = Tarefa.objects.filter(projeto=projeto).count()
    total_ideias = Ideia.objects.filter(projeto=projeto).count()
    total_anotacoes = Anotacao.objects.filter(projeto=projeto).count()

    # Identificar membros do projeto e suas contribuições
    membros = projeto.membros.annotate(
        tarefas_concluidas=Count('tarefas', filter=Q(tarefas__projeto=projeto, tarefas__concluida=True)),
        tarefas_totais=Count('tarefas', filter=Q(tarefas__projeto=projeto)),
        ideias_sugeridas=Count('ideia', filter=Q(ideia__projeto=projeto)),
        anotacoes_criadas=Count('anotacoes', filter=Q(anotacoes__projeto=projeto))
    ).order_by('-tarefas_totais', '-ideias_sugeridas', '-anotacoes_criadas')

    context = {
        'projeto': projeto,
        'total_tarefas': total_tarefas,
        'total_ideias': total_ideias,
        'total_anotacoes': total_anotacoes,
        'membros': membros,
    }

    return render(request, 'relatorios.html', context)


@login_required
def anotacoes_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id, usuario=request.user)
    tarefas = Tarefa.objects.filter(projeto=projeto)
    return render(request, 'DadosProjetos/anotacoes.html', {'projeto': projeto, 'tarefas': tarefas})

#---------------------------------------------------------------------------------------

def convidar_usuarios(request, projeto_id):
    projeto = Projeto.objects.get(id=projeto_id)
    buscar = request.GET.get('buscar', '')
    usuarios = User.objects.filter(username__icontains=buscar)
    return render(request, 'convidar_usuario.html', {
        'projeto': projeto,
        'usuarios': usuarios,
        'buscar': buscar,
    })

@login_required
def enviar_convite(request, projeto_id, usuario_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    usuario = get_object_or_404(User, id=usuario_id)
    if Convite.objects.filter(projeto=projeto, convidado=usuario).exists():
        messages.error(request, f"{usuario.username} já foi convidado para este projeto.")
        return redirect('notificacoes')

    convite = Convite.objects.create(
        projeto=projeto,
        convidado=usuario,
        enviado_por=request.user
    )

    link_projeto = reverse('detalhes_projeto', args=[projeto.id])
    Notificacao.objects.create(
        usuario=usuario,
        mensagem=f"Você foi convidado para participar do projeto {projeto.nome}.",
        convite=convite,
        link=link_projeto
    )

    messages.success(request, f"Convite enviado com sucesso para {usuario.username}!")

    return redirect('notificacoes')

@login_required
def aceitar_convite(request, convite_id):
    convite = get_object_or_404(Convite, id=convite_id)
    projeto = convite.projeto

    if request.method == "POST":
        convite.status = 'aceito'
        convite.save()


        projeto.membros.add(convite.convidado)
        Notificacao.objects.filter(convite=convite).update(lida=True)
        Notificacao.objects.create(
            usuario=convite.enviado_por,
            mensagem=f"{convite.convidado.username} aceitou o convite para o projeto {projeto.nome}.",
            convite=convite
        )

        messages.success(request, "Convite aceito com sucesso!")
        return redirect('notificacoes')

@login_required
def recusar_convite(request, convite_id):
    convite = get_object_or_404(Convite, id=convite_id)

    if request.method == "POST":
        convite.status = 'recusado'
        convite.save()
        Notificacao.objects.create(
            usuario=convite.enviado_por,
            mensagem=f"{convite.convidado.username} recusou o convite para o projeto {convite.projeto.nome}.",
            convite=convite
        )

        Notificacao.objects.filter(convite=convite).delete()

        messages.info(request, "Convite recusado!")
        return redirect('notificacoes')



@login_required
def marcar_tarefa_concluida(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    if tarefa.projeto.responsavel != request.user and request.user not in tarefa.projeto.membros.all():
        return HttpResponseForbidden("Você não tem permissão para modificar esta tarefa.")
    tarefa.concluida = True
    tarefa.save()
    return redirect('detalhes_projeto', projeto_id=tarefa.projeto.id)

@login_required
def desmarcar_tarefa_concluida(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    if tarefa.projeto.responsavel != request.user and request.user not in tarefa.projeto.membros.all():
        return HttpResponseForbidden("Sem permissão para modificar.")
    tarefa.concluida = False
    tarefa.save()
    return redirect('detalhes_projeto', projeto_id=tarefa.projeto.id)


@login_required
def excluir_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    if tarefa.projeto.responsavel != request.user and request.user not in tarefa.projeto.membros.all():
        return HttpResponseForbidden("Sem permissão para excluir.")
    projeto_id = tarefa.projeto.id
    tarefa.delete()
    return redirect('detalhes_projeto', projeto_id=projeto_id)
