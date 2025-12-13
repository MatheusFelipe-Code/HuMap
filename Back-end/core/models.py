# core/models.py
from django.db import models
from django.conf import settings # Importação necessária para referenciar o usuário

class Denuncia(models.Model):
    TIPO_CHOICES = [
        ('violencia', 'Violência Urbana'),
        ('saneamento', 'Saneamento Básico'),
        ('planejamento', 'Infraestrutura e Mobilidade'),
        ('meioambiente', 'Meio Ambiente'),
    ]

    # Campo novo para vincular a denúncia ao usuário que a criou
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    subtema = models.CharField(max_length=100, blank=True, null=True)
    descricao = models.TextField()
    
    # Campos de localização (Latitude e Longitude)
    # Aumentado para suportar maior precisão vinda do Leaflet sem arredondar no front
    latitude = models.DecimalField(max_digits=20, decimal_places=15, null=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=15, null=True)
    
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - {self.data_criacao}"

class AnexoDenuncia(models.Model):
    """
    Modelo para armazenar as fotos anexadas a uma denúncia.
    """
    denuncia = models.ForeignKey(Denuncia, related_name='anexos', on_delete=models.CASCADE)
    arquivo = models.ImageField(upload_to='denuncias/%Y/%m/')
    uploaded_at = models.DateTimeField(auto_now_add=True)