from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import register

urlpatterns = [
    path('', views.index, name='index'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),  # Para "Meu Perfil"
    path('notificacoes/', views.notificacoes, name='notificacoes'), 
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('projetos/novo/', views.criar_projeto, name='criar_projeto'),

    path('convidar_usuarios/<int:projeto_id>/', views.convidar_usuarios, name='convidar_usuarios'),
    path('enviar_convite/<int:projeto_id>/<int:usuario_id>/', views.enviar_convite, name='enviar_convite'),
    path('aceitar_convite/<int:convite_id>/', views.aceitar_convite, name='aceitar_convite'),
    path('recusar_convite/<int:convite_id>/', views.recusar_convite, name='recusar_convite'),

    path('register/', register, name='register'),
    path('excluir_projeto/<int:projeto_id>/', views.excluir_projeto, name='excluir_projeto'),
    path('criar_projeto/', views.criar_projeto, name='criar_projeto'),
    path('projeto/<int:projeto_id>/adicionar_tarefa/', views.adicionar_tarefa, name='adicionar_tarefa'),

    path('marcar_como_lida/<int:notificacao_id>/', views.marcar_como_lida, name='marcar_como_lida'),
    path('notificacoes/', views.notificacoes, name='notificacoes'),

    path('relatorios/<int:projeto_id>/', views.relatorios, name='relatorios'),

    path('detalhes_projeto/<int:projeto_id>/', views.detalhes_projeto, name='detalhes_projeto'),

    path('adicionar_ideia/<int:projeto_id>/', views.adicionar_ideia, name='adicionar_ideia'),
    path('adicionar_nota/<int:projeto_id>/', views.adicionar_nota, name='adicionar_nota'),
    path('excluir-projeto/<int:projeto_id>/', views.excluir_projeto, name='excluir_projeto'),

    path('marcar_ideia_concluida/<int:ideia_id>/', views.marcar_ideia_concluida, name='marcar_ideia_concluida'),
    path('desmarcar_ideia_concluida/<int:ideia_id>/', views.desmarcar_ideia_concluida, name='desmarcar_ideia_concluida'),
    path('marcar_anotacao_concluida/<int:anotacao_id>/', views.marcar_anotacao_concluida, name='marcar_anotacao_concluida'),
    path('desmarcar_anotacao_concluida/<int:anotacao_id>/', views.desmarcar_anotacao_concluida, name='desmarcar_anotacao_concluida'),


    path('excluir_ideia/<int:ideia_id>/', views.excluir_ideia, name='excluir_ideia'),
    path('excluir_anotacao/<int:anotacao_id>/', views.excluir_anotacao, name='excluir_anotacao'),

    path('projeto/<int:projeto_id>/anotacoes/', views.anotacoes_projeto, name='anotacoes_projeto'),
    path('adicionar_tarefa/<int:projeto_id>/', views.adicionar_tarefa, name='adicionar_tarefa'),

    path('tarefa/<int:tarefa_id>/concluir/', views.marcar_tarefa_concluida, name='marcar_tarefa_concluida'),
    path('tarefa/<int:tarefa_id>/excluir/', views.excluir_tarefa, name='excluir_tarefa'),
    path('tarefa/<int:tarefa_id>/desmarcar/', views.desmarcar_tarefa_concluida, name='desmarcar_tarefa_concluida'),
]
