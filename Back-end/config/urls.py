"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.views.static import serve
from core.views import sobre_view

urlpatterns = [
    # --- ROTA DA PÁGINA INICIAL ---
    # Quando acessar a raiz (vazio), redireciona para o Login
    path('', RedirectView.as_view(url='/users/login/', permanent=False)),

    # Painel Administrativo do Django
    path('admin/', admin.site.urls),

    # App Core: Contém Home, Suporte, Configurações, Feed e a API de Denúncias.
    path('', include('core.urls')), 

    # App Users: Contém Login, Cadastro e Perfil.
    path('users/', include('users.urls')),

    # Rota específica para a página "Sobre Nós"
    path('sobre/', sobre_view, name='sobre_nos'),

    # Rota de compatibilidade
    path('info/', include(('core.urls', 'info'), namespace='info')),
    
    # --- ROTA PARA SERVIR ARQUIVOS DE MÍDIA (FOTOS) NO RENDER ---
    # Isso garante que as fotos de perfil e denúncias apareçam mesmo com DEBUG=False
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
]

# --- SERVIR ARQUIVOS ESTÁTICOS (CSS/JS) EM MODO DEBUG ---
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])