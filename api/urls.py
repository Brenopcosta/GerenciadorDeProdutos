from django.urls import path
from api.views import retorna_todos_os_produtos
from api.views import cria_novo_produto
from api.views import listar_detalhes_do_produto
from api.views import deletar_produto
from api.views import altera_produto
from api.views import retorna_todos_os_pedidos_do_usuario
from api.views import cria_novo_pedido
from api.views import deletar_pedido
from api.views import loginNoSistema
from api.views import detalhes_do_pedido
from api.views import alterar_pedido
from api.views import pagar_pedido

app_name = 'api'

urlpatterns = [
    path('login/', loginNoSistema, name='login'),
    path('produtos/', retorna_todos_os_produtos, name='todos'),
    path('criaProduto/', cria_novo_produto, name='criaNovoProduto'),
    path('detalhesDoProduto/<int:idDoProduto>', listar_detalhes_do_produto, name='detalhesDoProduto'),
    path('deletarProduto/<int:idDoProduto>', deletar_produto, name='deletarDoProduto'),
    path('atualizaProduto/<int:idDoProduto>', altera_produto, name='atualizaProduto'),
    path('listaPedidos/', retorna_todos_os_pedidos_do_usuario, name='listaPedidos'),
    path('criaPedido/', cria_novo_pedido, name='criaPedido'),
    path('deletarPedido/<int:idDoPedido>', deletar_pedido, name='deletarPedido'),
    path('detalhesDoPedido/<int:idDoPedido>', detalhes_do_pedido, name='detalharPedido'),
    path('alterarPedido/<int:idDoPedido>', alterar_pedido, name='alterarPedido'),
    path('pagarPedido/<int:idDoPedido>', pagar_pedido, name='pagarPedido'),   
]
