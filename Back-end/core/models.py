from django.db import models
from django.conf import settings  # Para referenciar o usuário

class Denuncia(models.Model):
    TIPO_CHOICES = [
        ('violencia', 'Violência Urbana'),
        ('saneamento', 'Saneamento Básico'),
        ('planejamento', 'Infraestrutura e Mobilidade'),
        ('meioambiente', 'Meio Ambiente'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    subtema = models.CharField(max_length=100, blank=True, null=True)
    descricao = models.TextField()

    # Localização
    latitude = models.DecimalField(max_digits=20, decimal_places=15, null=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=15, null=True)
    
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - {self.data_criacao}"


class AnexoDenuncia(models.Model):
    """
    Fotos anexadas a uma denúncia.
    """
    denuncia = models.ForeignKey(Denuncia, related_name='anexos', on_delete=models.CASCADE)
    arquivo = models.ImageField(upload_to='denuncias/%Y/%m/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class LikeDenuncia(models.Model):
    """
    Curtidas de usuários em denúncias.
    Cada usuário pode curtir uma denúncia apenas uma vez.
    """
    denuncia = models.ForeignKey(Denuncia, related_name='likes', on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('denuncia', 'usuario')  # Garante curtida única

    def __str__(self):
        return f"{self.usuario.email} curtiu {self.denuncia.id}"


class ComentarioDenuncia(models.Model):
    """
    Comentários persistentes de usuários em denúncias.
    """
    denuncia = models.ForeignKey(Denuncia, related_name='comentarios', on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.email} comentou na denúncia {self.denuncia.id}"
