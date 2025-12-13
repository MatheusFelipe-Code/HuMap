from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions # Adicionado permissions aqui
from .serializers import CadastroSerializer, UserSerializer # Adicionado UserSerializer aqui (crie-o se não existir)
from .models import User # Importação do modelo User

# --- VIEWS DE RENDERIZAÇÃO E LÓGICA DE USUÁRIO ---

def cadastro_view(request):
    """
    Renderiza a página HTML de cadastro.
    """
    return render(request, 'Pages/Cadastro/cadastro.html')

class CadastroView(APIView):
    """
    API que recebe os dados do formulário de cadastro via JSON (POST),
    valida e cria o usuário no banco de dados.
    """
    def post(self, request):
        serializer = CadastroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Usuário criado com sucesso!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def login_view(request):
    """
    Gerencia o Login:
    - GET: Mostra a tela de login.
    - POST: Processa a autenticação (Email + Senha).
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # O Django autentica usando 'username', mas configuramos para ser o email
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            # Redireciona para a Home (Mapa)
            return redirect('core:home')
        else:
            # Se falhar, volta para o login
            return render(request, 'Pages/Login/login.html', {'error': 'Email ou senha inválidos'})
    
    return render(request, 'Pages/Login/login.html')

def logout_view(request):
    """
    Desloga o usuário e manda de volta para o login.
    """
    logout(request)
    return redirect('users:login')

@login_required
def perfil_view(request):
    """
    Renderiza a página de perfil (Apenas se estiver logado).
    """
    return render(request, 'Pages/Perfil/perfil.html')

# --- NOVA VIEW: RECUPERAÇÃO DE CONTA ---
def recuperacao_view(request):
    """
    Renderiza a tela de recuperação de senha.
    """
    return render(request, 'Pages/Recuperação/recuperacao.html')

# --- NOVA VIEW: ATUALIZAR PERFIL (FOTO) ---
class AtualizarPerfilView(APIView):
    """
    API para atualizar a foto de perfil (e outros dados se necessário).
    Requer autenticação.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        # data = request.data  # Pode ser usado para atualizar outros campos textuais
        
        # Atualiza a foto se ela vier na requisição
        if 'foto' in request.FILES:
            user.foto = request.FILES['foto']
        
        # Exemplo: Atualizar outros campos se desejar
        # if 'first_name' in request.data: 
        #     user.first_name = request.data['first_name']
        
        user.save()
        return Response({
            "mensagem": "Perfil atualizado com sucesso!", 
            "foto_url": user.get_foto_url()
        }, status=status.HTTP_200_OK)