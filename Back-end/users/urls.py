from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Rotas de Páginas (HTML)
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('recuperacao/', views.recuperacao_view, name='user_recuperacao'),
    
    # Rotas de API (JSON para JavaScript)
    path('api/cadastro/', views.CadastroView.as_view(), name='api_cadastro'),
    path('api/atualizar-perfil/', views.AtualizarPerfilView.as_view(), name='atualizar-perfil'),
]