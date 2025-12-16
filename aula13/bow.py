import math

# ------------------------------------------------------------
# 1. TEXTO BASE
# ------------------------------------------------------------
texto = """
o desenvolvimento de software moderno exige agilidade e colaboracao
linguagens como python e javascript sao cruciais
para construir aplicacoes web e mobile rapidas e seguras
a infraestrutura de cloud computing facilita a implantacao e a escalabilidade
machine learning e inteligencia artificial transformam dados em valor
"""

# ------------------------------------------------------------
# 2. CONSTRUÇÃO DO VOCABULÁRIO
# ------------------------------------------------------------

texto_minusculo = texto.lower()
lista_palavras = texto_minusculo.split()
vocabulario = []

for palavra in lista_palavras:
    if palavra not in vocabulario:
        vocabulario.append(palavra)

vocabulario.sort()

print("Vocabulário:")
print(vocabulario)
print("Tamanho do vocabulário:", len(vocabulario))
print()

# ------------------------------------------------------------
# 3. MAPEAMENTO: PALAVRA -> POSIÇÃO NO VETOR
# ------------------------------------------------------------

indice_palavra = {}
posicao = 0
for palavra in vocabulario:
    indice_palavra[palavra] = posicao
    posicao = posicao + 1

# ------------------------------------------------------------
# 4. FRASES DE ENTRADA
# ------------------------------------------------------------

frases = []
frases.append("python e javascript para aplicacoes web")
frases.append("cloud computing e escalabilidade de software")
frases.append("inteligencia artificial e machine learning transformam dados")
frases.append("desenvolvimento moderno exige agilidade e colaboracao")
frases.append("infraestrutura para aplicacoes rapidas e seguras")

# ------------------------------------------------------------
# 5. FUNÇÃO PARA CRIAR EMBEDDING BINÁRIO
# ------------------------------------------------------------

def criar_embedding_binario(frase, vocabulario, indice_palavra):
    vetor = []
    tamanho_vocabulario = len(vocabulario)

    contador = 0
    while contador < tamanho_vocabulario:
        vetor.append(0)
        contador = contador + 1

    frase_minuscula = frase.lower()
    palavras_frase = frase_minuscula.split()

    for palavra in palavras_frase:
        if palavra in indice_palavra:
            pos = indice_palavra[palavra]
            vetor[pos] = 1

    return vetor

# ------------------------------------------------------------
# 6. CRIAÇÃO DOS EMBEDDINGS DAS FRASES
# ------------------------------------------------------------

embeddings = []

for frase in frases:
    vetor_frase = criar_embedding_binario(frase, vocabulario, indice_palavra)
    embeddings.append(vetor_frase)

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
