# ============================================================
# EXEMPLO DIDÁTICO: BAG OF WORDS BINÁRIO E DISTÂNCIA EUCLIDIANA
# ============================================================

# Importamos a biblioteca matemática apenas para usar a raiz quadrada
import math

# ------------------------------------------------------------
# 1. TEXTO BASE
# ------------------------------------------------------------
# Texto que será usado para extrair o vocabulário
texto = """
aprendizado de maquina e inteligencia artificial
sao areas importantes da computacao
aprendizado supervisionado e nao supervisionado
"""

# ------------------------------------------------------------
# 2. CONSTRUÇÃO DO VOCABULÁRIO
# ------------------------------------------------------------

# Transformamos todo o texto em letras minúsculas
texto_minusculo = texto.lower()

# Quebramos o texto em palavras usando espaço como separador
lista_palavras = texto_minusculo.split()

# Criamos uma lista vazia para armazenar o vocabulário
vocabulario = []

# Percorremos todas as palavras do texto
for palavra in lista_palavras:
    # Verificamos se a palavra ainda não está no vocabulário
    if palavra not in vocabulario:
        # Se não estiver, adicionamos
        vocabulario.append(palavra)

# Ordenamos o vocabulário em ordem alfabética
vocabulario.sort()

# Exibimos o vocabulário
print("Vocabulário:")
print(vocabulario)
print("Tamanho do vocabulário:", len(vocabulario))
print()

# ------------------------------------------------------------
# 3. MAPEAMENTO: PALAVRA -> POSIÇÃO NO VETOR
# ------------------------------------------------------------

# Criamos um dicionário vazio
indice_palavra = {}

# Para cada posição do vocabulário
posicao = 0
for palavra in vocabulario:
    indice_palavra[palavra] = posicao
    posicao = posicao + 1

# ------------------------------------------------------------
# 4. FRASES DE ENTRADA
# ------------------------------------------------------------
# Todas as palavras DEVEM existir no vocabulário

frases = []
frases.append("aprendizado de maquina")
frases.append("inteligencia artificial")
frases.append("aprendizado supervisionado")
frases.append("nao supervisionado")
frases.append("computacao e inteligencia")

# ------------------------------------------------------------
# 5. FUNÇÃO PARA CRIAR EMBEDDING BINÁRIO
# ------------------------------------------------------------

def criar_embedding_binario(frase, vocabulario, indice_palavra):
    # Criamos um vetor cheio de zeros
    vetor = []
    tamanho_vocabulario = len(vocabulario)

    contador = 0
    while contador < tamanho_vocabulario:
        vetor.append(0)
        contador = contador + 1

    # Colocamos a frase em minúsculas
    frase_minuscula = frase.lower()

    # Quebramos a frase em palavras
    palavras_frase = frase_minuscula.split()

    # Para cada palavra da frase
    for palavra in palavras_frase:
        # Descobrimos a posição da palavra no vetor
        pos = indice_palavra[palavra]

        # Marcamos presença da palavra com 1
        vetor[pos] = 1

    return vetor

# ------------------------------------------------------------
# 6. CRIAÇÃO DOS EMBEDDINGS DAS FRASES
# ------------------------------------------------------------

embeddings = []

for frase in frases:
    vetor_frase = criar_embedding_binario(frase, vocabulario, indice_palavra)
    embeddings.append(vetor_frase)

# Exibimos os embeddings
print("Embeddings binários das frases:")
contador = 1
for vetor in embeddings:
    print("Frase", contador, ":", vetor)
    contador = contador + 1
print()

# ------------------------------------------------------------
# 7. FUNÇÃO PARA CALCULAR DISTÂNCIA EUCLIDIANA
# ------------------------------------------------------------

def distancia_euclidiana(vetor1, vetor2):
    soma = 0
    tamanho = len(vetor1)

    indice = 0
    while indice < tamanho:
        diferenca = vetor1[indice] - vetor2[indice]
        soma = soma + (diferenca * diferenca)
        indice = indice + 1

    distancia = math.sqrt(soma)
    return distancia

# ------------------------------------------------------------
# 8. MATRIZ DE DISTÂNCIAS (5 x 5)
# ------------------------------------------------------------

print("Matriz de distâncias euclidianas:")

linha = 0
while linha < 5:
    coluna = 0
    while coluna < 5:
        d = distancia_euclidiana(embeddings[linha], embeddings[coluna])
        print("{:.2f}".format(d), end="\t")
        coluna = coluna + 1
    print()
    linha = linha + 1
