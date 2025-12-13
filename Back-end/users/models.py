from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Campos extras que seu formulário pede
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    receber_notificacoes = models.BooleanField(default=False)

    # NOVO CAMPO: Foto de Perfil
    # As imagens serão salvas na pasta 'media/perfil_fotos/'
    # CORREÇÃO: Removido o default para que o usuário comece sem foto (null)
    foto = models.ImageField(upload_to='perfil_fotos/', blank=True, null=True)

    # Vamos usar o email como login principal em vez do 'username'
    email = models.EmailField(unique=True)
    
    # Configurações para logar com email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name'] # username ainda é obrigatório no banco, mas geraremos auto

    def __str__(self):
        return self.email

    def get_foto_url(self):
        """
        Retorna a URL da foto se existir, caso contrário retorna None.
        Isso ajuda no template a decidir se mostra a foto do usuário ou a padrão.
        """
        # Verifica se existe foto e se ela tem um atributo url válido
        if self.foto and hasattr(self.foto, 'url'):
            return self.foto.url
        return None