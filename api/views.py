import secrets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.models import Produto
from api.models import Pedidos
from api.models import Usuario
from api.serializers import ProdutoSerializer
from api.serializers import PedidosSerializer


token_userID = dict([])

@api_view(['POST',  ])
def loginNoSistema(request):
    usuario = Usuario.objects.filter(nomeDeUsuario=request.data['nomeUsuario'], senha=request.data['senha'])[0]
    if usuario:
        token=secrets.token_hex(16)
        token_userID[token] = usuario.id
        return Response(token,status=status.HTTP_200_OK)
    else:
        return Response(token,status=status.HTTP_404_NOT_FOUND)



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

#TOFIX 
@api_view(['PATCH',  ])
def altera_produto(request, idDoProduto):
    produtoSerializado = ProdutoSerializer(Produto, data=request.data)
    if produtoSerializado.is_valid():
        instanciaDoProduto = Produto.objects.get(id=idDoProduto)
        produtoSerializado.update(instanciaDoProduto, produtoSerializado.data)
        return Response(produtoSerializado.data, status=status.HTTP_201_CREATED) 
    return Response(produtoSerializado.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET',  ])
def retorna_todos_os_pedidos(request):
    pedidos = Pedidos.objects.all()
    pedidosSerializado = PedidosSerializer(pedidos, many=True)
    return Response(pedidosSerializado.data, status=status.HTTP_200_OK)

@api_view(['POST',  ])
def cria_novo_pedido(request):
    pedidoSerializado = PedidosSerializer(data=request.data)
    if pedidoSerializado.is_valid():
        pedidoSerializado.save()
        return Response(pedidoSerializado.data, status=status.HTTP_201_CREATED) 
    return Response(pedidoSerializado.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE',  ])
def deletar_pedido(request, idDoPedido):
    try: 
        Pedidos.objects.get(id=idDoPedido).delete()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET',  ])
def listar_detalhes_do_pedido(request, idDoPedido):
    try: 
        pedidoSerializado=PedidosSerializer(Pedidos.objects.get(id=idDoPedido)).data    
        return Response(pedidoSerializado, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)