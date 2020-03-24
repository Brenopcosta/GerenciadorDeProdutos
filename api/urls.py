from django.urls import path
from api.views import retorna_todos_os_produtos
from api.views import cria_novo_produto

app_name = 'api'

urlpatterns = [
    path('produtos/', retorna_todos_os_produtos, name='todos'),
    path('criaProduto/', cria_novo_produto, name='criaNovoProduto'),

]
