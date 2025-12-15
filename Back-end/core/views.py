from django.shortcuts import render, get_object_or_404
from .models import Denuncia, LikeDenuncia, ComentarioDenuncia
from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import DenunciaSerializer
from django.contrib.auth.decorators import login_required



def home_view(request):
    return render(request, 'Pages/home/home.html')


def suporte_view(request):
    return render(request, 'Pages/Suporte/suporte.html')


def configuracao_view(request):
    return render(request, 'Pages/Configuracao/configuracao.html')


def tutorial_view(request):
    return render(request, 'Pages/Tutorial/tutorial.html')


def sobre_view(request):
    return render(request, 'Pages/SobreNos/sobre.html')


@login_required
def feed_view(request):
    """
    Feed com:
    - Curtidas (toggle)
    - Comentários via POST
    """
    if request.method == 'POST':
        denuncia_id = request.POST.get('curtir_denuncia_id')
        comentario_texto = request.POST.get('comentario_texto')

        if denuncia_id:
            denuncia = get_object_or_404(Denuncia, id=denuncia_id)

            # ===== COMENTÁRIO =====
            if comentario_texto:
                ComentarioDenuncia.objects.create(
                    denuncia=denuncia,
                    usuario=request.user,
                    texto=comentario_texto
                )

            # ===== CURTIDA =====
            else:
                like, created = LikeDenuncia.objects.get_or_create(
                    denuncia=denuncia,
                    usuario=request.user
                )
                if not created:
                    like.delete()

    # ===== CARREGAR FEED =====
    denuncias = Denuncia.objects.all().order_by('-data_criacao')

    for d in denuncias:
        d.curtidas_count = d.likes.count()
        d.usuario_curtiu = d.likes.filter(usuario=request.user).exists()
        d.comentarios_list = d.comentarios.select_related('usuario').all()

    return render(request, 'Pages/Feed/feed.html', {'denuncias': denuncias})


# ================= API =================

class DenunciaListCreateView(generics.ListCreateAPIView):
    queryset = Denuncia.objects.all().order_by('-data_criacao')
    serializer_class = DenunciaSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(usuario=self.request.user)
        else:
            serializer.save()
