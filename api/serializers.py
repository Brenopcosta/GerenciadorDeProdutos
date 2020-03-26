from rest_framework import serializers
from api.models import Produto
from api.models import Pedidos
from api.models import Usuario

class ProdutoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model =  Produto
        fields = ['id', 'nome', 'descricao', 'preco', 'dataDeCriacao', 'estoque']
    
    def update(self, instance, validated_data):
        instance.nome = validated_data['nome']
        instance.descricao = validated_data['descricao']
        instance.preco = validated_data['preco']
        instance.estoque = validated_data['estoque']
        instance.save()
        return instance

class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= Produto
        fields = ['id', 'nomeDeUsuario', 'senha', 'email', 'primeiroNome', 'utlimoNome', 'enredeco']



class PedidosSerializer(serializers.ModelSerializer):
    class Meta:
        model= Pedidos
        fields = ['id', 'produto', 'usuario', 'quantidadeDeItens', 'precoTotal', 'pago']   