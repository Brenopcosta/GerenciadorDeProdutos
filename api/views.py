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

def usuarioJaLogado(idDoUsuario):
    return idDoUsuario in token_userID.values()

def autenticar(headers):
        try:
            idUsusario = token_userID[headers['token']]
            return idUsusario
        except:
            return 0

def decrementaEstoqueDoProduto(idDoProduto, quantidadeASerDecrementada):
    produto = Produto.objects.get(id=idDoProduto)
    if produto.estoque >= quantidadeASerDecrementada:
        produto.estoque = produto.estoque-quantidadeASerDecrementada
        produto.save()
    else:
        raise ValueError('Valor requerido maior que o estoque')


def incrementaEstoqueDoProduto(idDoProduto, quantidadeASerIncrementada):
    produto = Produto.objects.get(id=idDoProduto)
    produto.estoque = produto.estoque+quantidadeASerIncrementada
    produto.save()

@api_view(['POST',  ])
def loginNoSistema(request):
    try:
        usuario = Usuario.objects.filter(nomeDeUsuario=request.data['nomeUsuario'], senha=request.data['senha'])[0]
        if usuarioJaLogado(usuario.id)==False:
            token=secrets.token_hex(16)
            token_userID[token] = usuario.id
            return Response(token,status=status.HTTP_200_OK)
        else:
            return Response(status.HTTP_208_ALREADY_REPORTED)
    except IndexError:
        return Response(status=status.HTTP_404_NOT_FOUND)

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
    if autenticar(request.headers):
        produtoSerializado = ProdutoSerializer(data=request.data)
        if produtoSerializado.is_valid():
            produtoSerializado.save()
            return Response(produtoSerializado.data, status=status.HTTP_201_CREATED) 
        return Response(produtoSerializado.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_401_UNAUTHORIZED)
        

@api_view(['DELETE',  ])
def deletar_produto(request, idDoProduto):
    if autenticar(request.headers):
        try: 
            Produto.objects.get(id=idDoProduto).delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['PATCH',  ])
def altera_produto(request, idDoProduto):
    if autenticar(request.headers):
        produtoASerAtualizado=Produto.objects.get(id=idDoProduto)
        try:
            produtoASerAtualizado.nome = request.data['nome']
            produtoASerAtualizado.descricao = request.data['descricao']
            produtoASerAtualizado.preco = request.data['preco']
            produtoASerAtualizado.estoque = request.data['estoque']
            produtoASerAtualizado.save()
            return Response(ProdutoSerializer(produtoASerAtualizado).data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET',  ])
def retorna_todos_os_pedidos_do_usuario(request):
    idDoUsuario = autenticar(request.headers)
    if idDoUsuario:
        pedidos = Pedidos.objects.filter(usuario_id=idDoUsuario)
        pedidosSerializado = PedidosSerializer(pedidos, many=True)
        return Response(pedidosSerializado.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST',  ])
def cria_novo_pedido(request):
    idDoUsuario = autenticar(request.headers)
    if idDoUsuario:
        decrementaEstoqueDoProduto(request.data['produto'],request.data['quantidadeDeItens'])
        pedido = Pedidos()
        pedido.usuario=Usuario.objects.get(id=idDoUsuario)
        pedido.produto=Produto.objects.get(id=request.data['produto'])
        pedido.quantidadeDeItens=request.data['quantidadeDeItens']
        pedido.precoTotal = pedido.produto.preco * pedido.quantidadeDeItens
        pedido.pago = False
        pedido.save()
        return Response(PedidosSerializer(pedido).data, status=status.HTTP_201_CREATED)   
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['DELETE',  ])
def deletar_pedido(request, idDoPedido):
    idDoUsuario = autenticar(request.headers)
    if idDoUsuario:
        try: 
            Pedidos.objects.filter(id=idDoPedido, usuario = idDoUsuario)[0].delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET',  ])
def detalhes_do_pedido(request, idDoPedido):
    idDoUsuario = autenticar(request.headers)
    if idDoUsuario:
        try: 
            pedidoSerializado=PedidosSerializer(Pedidos.objects.filter(id=idDoPedido, usuario = idDoUsuario)[0]).data    
            return Response(pedidoSerializado, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PATCH',  ])
def alterar_pedido(request, idDoPedido):
    idDoUsuario = autenticar(request.headers)
    if idDoUsuario:
        pedido = Pedidos.objects.filter(id=idDoPedido, usuario = idDoUsuario)[0]
        if pedido.quantidadeDeItens < request.data['quantidadeDeItens']:
            decrementaEstoqueDoProduto(pedido.produto.id, request.data['quantidadeDeItens'] - pedido.quantidadeDeItens)
            pedido.quantidadeDeItens = request.data['quantidadeDeItens']
            pedido.precoTotal = pedido.produto.preco * pedido.quantidadeDeItens 
            pedido.save()
            return Response(PedidosSerializer(pedido).data, status=status.HTTP_200_OK)
        else:
            incrementaEstoqueDoProduto(pedido.produto.id, pedido.quantidadeDeItens - request.data['quantidadeDeItens'])
            pedido.quantidadeDeItens = request.data['quantidadeDeItens']
            pedido.precoTotal = pedido.produto.preco * pedido.quantidadeDeItens 
            pedido.save()
            return Response(PedidosSerializer(pedido).data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['PATCH',  ])
def pagar_pedido(request, idDoPedido):
    idDoUsuario = autenticar(request.headers)
    if idDoUsuario:
        pedido = Pedidos.objects.filter(id=idDoPedido, usuario = idDoUsuario)[0]    
        pedido.pago = True
        pedido.save()
        return Response(PedidosSerializer(pedido).data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_401_UNAUTHORIZED)
