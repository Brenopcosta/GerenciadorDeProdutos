from django.urls import path
from api.views import retorna_todos_os_produtos
from api.views import cria_novo_produto
from api.views import listar_detalhes_do_produto
from api.views import deletar_produto
from api.views import altera_produto
from api.views import retorna_todos_os_pedidos
from api.views import cria_novo_pedido
from api.views import deletar_pedido
from api.views import loginNoSistema

app_name = 'api'

urlpatterns = [
    path('login/', loginNoSistema, name='login'),
    path('produtos/', retorna_todos_os_produtos, name='todos'),
    path('criaProduto/', cria_novo_produto, name='criaNovoProduto'),
    path('detalhesDoProduto/<int:idDoProduto>', listar_detalhes_do_produto, name='detalhesDoProduto'),
    path('deletarProduto/<int:idDoProduto>', deletar_produto, name='deletarDoProduto'),
    path('atualizaProduto/<int:idDoProduto>', altera_produto, name='atualizaProduto'),
    path('listaPedidos/', retorna_todos_os_pedidos, name='listaPedidos'),
    path('criaPedido/', cria_novo_pedido, name='criaPedido'),
    path('deletarPedido/<int:idDoPedido>', deletar_pedido, name='deletarPedido'),
]
