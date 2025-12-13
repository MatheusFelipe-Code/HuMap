"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView # Necessário para o redirecionamento inicial
from core.views import sobre_view # Importamos a view específica para a rota avulsa

urlpatterns = [
    # --- ROTA DA PÁGINA INICIAL ---
    # Quando acessar http://127.0.0.1:8000/ (vazio), redireciona automaticamente para o Login
    path('', RedirectView.as_view(url='/users/login/', permanent=False)),

    # Painel Administrativo do Django
    path('admin/', admin.site.urls),

    # App Core: Contém Home, Suporte, Configurações, Feed e a API de Denúncias.
    # Usamos '' (vazio) para que as rotas dele (ex: /home/, /feed/) fiquem na raiz do site.
    path('', include('core.urls')), 

    # App Users: Contém Login, Cadastro e Perfil.
    # As rotas ficarão como /users/login/, /users/cadastro/, etc.
    path('users/', include('users.urls')),

    # Rota específica para a página "Sobre Nós"
    path('sobre/', sobre_view, name='sobre_nos'),

    # Rota de compatibilidade: Caso algum link antigo use 'info:sobre',
    # isso garante que ele continue funcionando redirecionando para as urls do core.
    path('info/', include(('core.urls', 'info'), namespace='info')),
]

# --- SERVIR ARQUIVOS ESTÁTICOS E MÍDIA (DEBUG MODE) ---
if settings.DEBUG:
    # Serve arquivos de mídia (uploads de usuários)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Serve arquivos estáticos (CSS, JS, Imagens do Front-end)
    # Pega o primeiro caminho definido em STATICFILES_DIRS no settings.py (sua pasta src)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])