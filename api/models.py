from django.db import models
# Create your models here.

class Produto(models.Model):
    nome = models.CharField(max_length=50,null = False , blank = False)
    descricao = models.CharField(max_length=50,null = False , blank = False)
    preco = models.FloatField(max_value=None, min_value=None)
    dataDeCriacao = models.DateField(auto_now_add=True)
    estoque = models.IntegerField(default=0)

    def __str__(self):
        return self.nome

class Usuario(models.Model):
    nomeDeUsuario = models.CharField(max_length=50,null = False , blank = False)
    senha = models.CharField(max_length=50,null = False , blank = False)
    email = models.CharField(max_length=50,null = False , blank = False)
    primeiroNome = models.CharField(max_length=50,null = False , blank = False)
    ultimoNome = models.CharField(max_length=50,null = False , blank = False)
    endereco = models.CharField(max_length=50,null = False , blank = False)

    def __str__(self):
        return self.nomeDeUsuario

class Pedidos():
    produto = models.ForeignKey(Produto , on_delete = models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete = models.CASCADE)
    quantidadeDeItens = models.IntegerField(default=0)
    precoTotal = models.FloatField(default=0.0)
    pago = models.BooleanField(default=0)

