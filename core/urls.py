
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import register

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('projeto/<int:projeto_id>/', views.detalhes_projeto, name='detalhes_projeto'),
    path('register/', register, name='register'),
    path('excluir_projeto/<int:projeto_id>/', views.excluir_projeto, name='excluir_projeto'),
    path('criar_projeto/', views.criar_projeto, name='criar_projeto'),


    path('projeto/<int:projeto_id>/adicionar_tarefa/', views.adicionar_tarefa, name='adicionar_tarefa'),
    path('enviar_convite/<int:projeto_id>/', views.enviar_convite, name='enviar_convite'),
    path('notificacoes/', views.notificacoes, name='notificacoes'),
    path('aceitar_convite/<int:convite_id>/', views.aceitar_convite, name='aceitar_convite'),
    path('recusar_convite/<int:convite_id>/', views.recusar_convite, name='recusar_convite'),


    path('relatorios/<int:projeto_id>/', views.relatorios, name='relatorios'),


    path('detalhes_projeto/<int:projeto_id>/', views.detalhes_projeto, name='detalhes_projeto'),
    path('adicionar_ideia/<int:projeto_id>/', views.adicionar_ideia, name='adicionar_ideia'),
    path('adicionar_nota/<int:projeto_id>/', views.adicionar_nota, name='adicionar_nota'),
    path('projeto/<int:projeto_id>/anotacoes/', views.anotacoes_projeto, name='anotacoes_projeto'),
    path('adicionar_tarefa/<int:projeto_id>/', views.adicionar_tarefa, name='adicionar_tarefa'),

]

