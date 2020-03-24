from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.models import Produto
from api.serializers import ProdutoSerializer

@api_view(['GET',  ])
def retorna_todos_os_produtos(request):
    produto = Produto(nome='faca', descricao='umaFaca', preco=22.5, estoque=2)
    produtoSerializado = ProdutoSerializer(produto)
    return Response(produtoSerializado.data)

@api_view(['POST',  ])
def cria_novo_produto(request):
    produtoSerializado = ProdutoSerializer(data=request.data)
    if produtoSerializado.is_valid():
        produtoSerializado.save()
        return Response(produtoSerializado.data, status=status.HTTP_201_CREATED) 
    return Response(produtoSerializado.errors, status=status.HTTP_400_BAD_REQUEST)


