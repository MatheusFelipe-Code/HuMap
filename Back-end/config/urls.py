from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.views.static import serve
from core.views import sobre_view

urlpatterns = [
    # --- ROTA DA PÁGINA INICIAL ---
    # Quando acessar o site (vazio), manda direto para o Login
    path('', RedirectView.as_view(url='/users/login/', permanent=False)),

    # Painel Administrativo
    path('admin/', admin.site.urls),

    # App Core: Contém Home, Feed, Suporte, etc.
    # Note que usamos include com namespace 'core' implícito nas urls do app
    path('', include('core.urls')), 

    # App Users: Contém Login, Cadastro, Perfil
    path('users/', include('users.urls')),

    # Rota específica para a página "Sobre Nós" (acessível via /sobre/)
    path('sobre/', sobre_view, name='sobre_nos'),
    
    # Rota de compatibilidade (opcional, mantive do seu código)
    path('info/', include(('core.urls', 'info'), namespace='info')),

    # --- SERVIR ARQUIVOS DE MÍDIA (FOTOS) ---
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

# --- SERVIR ARQUIVOS ESTÁTICOS EM DEBUG ---
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])