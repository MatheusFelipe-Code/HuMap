from rest_framework import serializers
from .models import User

# --- SEU CÓDIGO ANTIGO (MANTIDO IGUAL) ---
class CadastroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    # Mapeia o campo 'nome' (do JSON/HTML) para 'first_name' (do Banco)
    nome = serializers.CharField(source='first_name', required=True)

    class Meta:
        model = User
        fields = ['nome', 'email', 'password', 'confirm_password', 'cpf', 'data_nascimento', 'telefone', 'receber_notificacoes']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "As senhas não coincidem."})
        return data

    def create(self, validated_data):
        # Remove a confirmação de senha
        validated_data.pop('confirm_password')
        
        # Cria o usuário usando o gerenciador padrão do Django para criptografar a senha
        user = User.objects.create_user(
            username=validated_data['email'], # Usa o email como username (obrigatório no Django)
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name'), # O 'source' transformou 'nome' em 'first_name' aqui
            cpf=validated_data.get('cpf'),
            data_nascimento=validated_data.get('data_nascimento'),
            telefone=validated_data.get('telefone'),
            receber_notificacoes=validated_data.get('receber_notificacoes', False)
        )
        return user

# --- CÓDIGO NOVO (ADICIONE AQUI NO FINAL) ---

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Aqui listamos os campos que queremos enviar para o front-end
        # Incluímos 'foto' para que a URL da imagem seja enviada
        fields = ['id', 'email', 'first_name', 'last_name', 'foto', 'cpf', 'telefone']