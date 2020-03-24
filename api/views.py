from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.models import Produto
from api.serializers import ProdutoSerializer

@api_view(['GET',  ])
def retorna_todos_os_produtos(request):
    produtos = Produto.objects.all()
    produtoSerializado = ProdutoSerializer(produtos, many=True)
    return Response(produtoSerializado.data, status=status.HTTP_200_OK)

@api_view(['GET',  ])
def listar_detalhes_do_produto(request, idDoProduto):
    return Response(ProdutoSerializer(Produto.objects.get(id=idDoProduto)).data, status=status.HTTP_200_OK)

@api_view(['POST',  ])
def cria_novo_produto(request):
    produtoSerializado = ProdutoSerializer(data=request.data)
    if produtoSerializado.is_valid():
        produtoSerializado.save()
        return Response(produtoSerializado.data, status=status.HTTP_201_CREATED) 
    return Response(produtoSerializado.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE',  ])
def deletar_produto(request, idDoProduto):
    try: 
        Produto.objects.get(id=idDoProduto).delete()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH',  ])
def altera_produto(request):
    produtoSerializado = ProdutoSerializer(data=request.data)
    if produtoSerializado.is_valid():
        produtoSerializado.update()
        return Response(produtoSerializado.data, status=status.HTTP_201_CREATED) 
    return Response(produtoSerializado.errors, status=status.HTTP_400_BAD_REQUEST)
