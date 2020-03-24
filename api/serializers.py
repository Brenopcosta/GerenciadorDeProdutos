from rest_framework import serializers
from api.models import Produto

class ProdutoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model =  Produto
        fields = ['id', 'nome', 'descricao', 'preco', 'dataDeCriacao', 'estoque']