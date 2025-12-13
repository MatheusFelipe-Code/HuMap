from rest_framework import serializers
from .models import Denuncia, AnexoDenuncia

class AnexoSerializer(serializers.ModelSerializer):
    """
    Serializer para as fotos anexadas à denúncia.
    """
    class Meta:
        model = AnexoDenuncia
        fields = ['id', 'arquivo']

class DenunciaSerializer(serializers.ModelSerializer):
    """
    Serializer principal para listar e criar denúncias.
    Gerencia também o upload de múltiplas imagens e a exibição do nome do autor.
    """
    # Exibe as fotos cadastradas (apenas leitura)
    anexos = AnexoSerializer(many=True, read_only=True)
    
    # Recebe novas fotos no upload (apenas escrita)
    imagens = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )
    
    # Campo calculado para mostrar quem fez a denúncia
    usuario_nome = serializers.SerializerMethodField()

    class Meta:
        model = Denuncia
        fields = [
            'id', 'tipo', 'subtema', 'descricao', 
            'latitude', 'longitude', 'data_criacao', 
            'anexos', 'imagens', 'usuario_nome'
        ]

    def get_usuario_nome(self, obj):
        """
        Retorna o primeiro nome do usuário ou parte do email
        caso o nome não esteja preenchido. Se não tiver usuário, retorna "Anônimo".
        """
        if obj.usuario:
            return obj.usuario.first_name or obj.usuario.email.split('@')[0]
        return "Anônimo"

    def create(self, validated_data):
        """
        Sobrescreve o método create padrão para lidar com o upload
        de múltiplas imagens separadamente da criação da denúncia.
        """
        # Retira a lista de imagens dos dados (pois o modelo Denuncia não tem esse campo direto)
        imagens_data = validated_data.pop('imagens', [])
        
        # Cria a denúncia com os dados restantes (texto, tipo, coordenadas, usuário)
        denuncia = Denuncia.objects.create(**validated_data)
        
        # Cria um objeto AnexoDenuncia para cada imagem enviada
        for imagem in imagens_data:
            AnexoDenuncia.objects.create(denuncia=denuncia, arquivo=imagem)
        
        return denuncia