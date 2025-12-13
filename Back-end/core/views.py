from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Denuncia
from .serializers import DenunciaSerializer

# --- VIEWS PARA RENDERIZAR PÁGINAS HTML ---

def home_view(request):
    # Renderiza a página principal com o mapa
    return render(request, 'Pages/home/home.html')

def suporte_view(request):
    # Renderiza a página de Suporte
    return render(request, 'Pages/Suporte/suporte.html')

def configuracao_view(request):
    # Renderiza a página de Configurações
    return render(request, 'Pages/Configuracao/configuracao.html')

def tutorial_view(request):
    # Renderiza a página de Tutorial
    return render(request, 'Pages/Tutorial/tutorial.html')

def feed_view(request):
    # Renderiza a página de Feed
    return render(request, 'Pages/Feed/feed.html')

def sobre_view(request):
    # Renderiza a página Sobre Nós
    return render(request, 'Pages/SobreNos/sobre.html')

# --- API (Lógica do Back-end) ---

class DenunciaListCreateView(generics.ListCreateAPIView):
    """
    API para listar e criar denúncias.
    - GET: Lista todas as denúncias (público)
    - POST: Cria uma nova denúncia (requer login)
    Aceita upload de arquivos (imagens) via MultiPartParser.
    """
    queryset = Denuncia.objects.all().order_by('-data_criacao')
    serializer_class = DenunciaSerializer
    
    # Permite receber formulários com arquivos (upload de fotos)
    parser_classes = (MultiPartParser, FormParser)
    
    # Configuração de Permissão:
    # - Leitura (GET): Permitido para todos (IsAuthenticatedOrReadOnly)
    # - Escrita (POST): Apenas usuários logados
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Essa função é chamada automaticamente ao criar uma denúncia.
        # Ela pega o usuário que está logado (self.request.user) 
        # e salva no campo 'usuario' da denúncia.
        
        # Nota: Certifique-se de ter adicionado o campo 'usuario' 
        # no seu models.py (core) para isso funcionar perfeitamente.
        if self.request.user.is_authenticated:
            serializer.save(usuario=self.request.user)
        else:
            serializer.save()