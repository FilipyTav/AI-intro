# 1. Analise o grafo:

    D
    |
    B --- E
   / \     \
  A   \     G
   \   \
    C---F

## Faça a busca por largura e altura definindo o nó A como partida. Liste a ordem dos nós visitados para cada algoritmo. Desenhe a árvore de busca e desenvolva neste exercício os passos realizados. Registre também a fila e a pilha. Não se esqueça de riscar na pilha/fila os elementos que você retirou.

-X- -> Nó X foi removido

Nós já na list não são adicionados novamente

- BFS:

* Iteração 0: Nó = A / Visitados = [A] / fila = [B, C]
* Iteração 1: Nó = B / Visitados = [A, B] / fila = [-B-, C, D, E, F]
* Iteração 2: Nó = C / Visitados = [A, B, C] / fila = [-C-, D, E, F]
* Iteração 3: Nó = D / Visitados = [A, B, C, D] / fila = [-D-, E, F]
* Iteração 4: Nó = E / Visitados = [A, B, C, D, E] / fila = [-E-, F, G]
* Iteração 5: Nó = F / Visitados = [A, B, C, D, E, F] / fila = [-F-, G]
* Iteração 6: Nó = G / Visitados = [A, B, C, D, E, F, G] / fila = [-G-]
* Final: Visitados = [A, B, C, D, E, F, G] / fila = [ ]

- DFS:

* Iteração 0: Nó = A / Visitados = [A] / pilha = [B, C]
* Iteração 1: Nó = C / Visitados = [A, C] / pilha = [B, -C-, F]
* Iteração 2: Nó = F / Visitados = [A, C, F] / pilha = [B, -F-]
* Iteração 3: Nó = B / Visitados = [A, C, F, B] / pilha = [-B-, D, E]
* Iteração 4: Nó = E / Visitados = [A, C, F, B, E] / pilha = [D, -E-, G]
* Iteração 5: Nó = G / Visitados = [A, C, F, B, E, G] / pilha = [D, -G-]
* Iteração 6: Nó = D / Visitados = [A, C, F, B, E, G, D] / pilha = [-D-]
* Final: Visitados = [A, C, F, B, E, G, D] / pilha = [ ]

# 2. Os Algoritmos Genéticos (AGs) são amplamente utilizados para resolver problemas de otimização complexos em diversas áreas, desde engenharia até sistemas biológicos. Considerando o funcionamento geral de um AG, explique de forma estruturada como os elementos abaixo influenciam o desempenho do algoritmo: 

Em sua resposta, utilize exemplos conceituais (não precisam ser numéricos) para ilustrar cada parte.

- Representação dos indivíduos (codificação)
    - Discuta como diferentes formas de representar soluções (binária, real, permutação etc. podem facilitar ou dificultar o processo evolutivo.

R: 
A forma de representar as soluções afeta diretamente a facilidade da evolução. Representações binárias podem gerar grandes mudanças no valor com pequenas mutações, dificultando problemas contínuos. 
Codificação real permite variações suaves, facilitando otimização em espaços contínuos. 
Representações por permutação (como em rotas) exigem operadores específicos, pois mutações ou crossovers comuns podem gerar soluções inválidas. A escolha correta da codificação torna a busca mais eficiente e reduz problemas como estagnação ou inviabilidade.

Um problema de ajustar parâmetros contínuos é difícil se representado em binário, porque pequenas mutações podem gerar saltos grandes. Em real, pequenas mudanças mantêm coerência e facilitam a evolução.

- Função de aptidão (fitness)
    - Explique por que uma função de aptidão mal definida pode prejudicar a convergência do AG e levar a soluções ruins.

R: A função de aptidão(fitness) é uma parte extremamente importante do algoritmo genético. Ela atribui uma pontuação para cada indivíduo em uma população, representando o quão 'adaptados' eles são. Assim, se a função for mal definida, o algoritmo não vai ser capaz de discernir e escolher realmente os melhores indivíduos da geração, fazendo com que soluções não ótimas(adaptadas) transmitam seus genes para a próxima geração, permitindo que as populações piorem ou se mantenham estagnadas a cada geração.

Por exemplo, se a aptidão recompensa apenas velocidade em um robô, mas ignora segurança, o AG pode encontrar soluções que são muito rápidas, porém colidem constantemente — uma convergência ruim por métrica mal definida.

- Seleção, crossover e mutação
    - Explique como o equilíbrio entre exploração e explotação depende desses operadores e como diferentes parametrizações podem alterar a trajetória evolutiva.

R: 
Seleção: Define quais indivíduos passam seus genes para a próxima geração.
Seleção muito forte (menos aptos dificilmente escolhidos) reduz diversidade e aumenta a explotação.
Seleção fraca (muitos escolhidos) mantém diversidade e favorece a exploração.

Crossover: Combina características de dois indivíduos.
Crossovers mais complexos (geram filhos bem diferentes dos pais) aumentam a exploração.
Crossovers mais simples reforçam a explotação.

Mutação: Mudanças aleatórias nos genes dos indivíduos, com certa probabilidade.
Taxas altas geram muita variação - exploração.
Taxas baixas mantêm estabilidade - explotação.

Todos esses operadores funcionam em conjunto no funcionamento do algoritmo, e suas parametrizações podem fazer com que as tendências mudem, de acordo com o que é desejado.

Com seleção muito forte, apenas 1 ou 2 indivíduos dominam a população, e o AG rapidamente converge para uma solução local.
Com mutação alta, a população muda tanto que parece “reiniciar” a cada geração, impedindo o melhoramento.

- Elitismo e diversidade populacional
    - Analise como o elitismo pode acelerar a convergência e, ao mesmo tempo, contribuir para a perda de diversidade, e discuta estratégias para evitar esse problema. 

R: Elitismo é a prática de manter os N melhores indivíduos de uma geração e adicioná-los à próxima geração, sem mudanças, assim preservando os melhores genes. 
Esse processo pode contribuir para a perda de diversidade pelo fato de manter indivíduos entre gerações, sem mudanças, ao invés de novos indivíduos com novos genes. Pouca diversidade acelera a convergência, o que pode fazer com que o algoritmo venha a convergir para a melhor solução local.
Para evitar esse problema, pode-se limitar a quantidade de indivíduos que são mantidos por elitismo ou pode-se os mutar se a diversidade ficar muito baixa.

Se sempre os 3 melhores indivíduos foram mantidos em todas as gerações, eles podem dominar cedo demais e fazer toda a população parecer com eles — perdendo diversidade.

# 3. Explique detalhadamente como o algoritmo de Descida da Colina funciona, incluindo a forma como uma solução inicial é escolhida, como seus vizinhos são avaliados e como a próxima solução é selecionada. Em seguida, discuta as limitações principais do método, abordando o problema dos ótimos locais, planaltos e ombros (ridges), e explique por que o algoritmo pode falhar em encontrar a solução ótima global. Por fim, apresente duas estratégias comuns para mitigar essas limitações (ex.: reinícios aleatórios, uso de temperatura, variações estocásticas etc.) e discuta em que contextos cada uma é mais apropriada.

Descida da Colina é um algoritmo de otimização e, portanto, busca sempre minimizar sua função de custo. 
O algoritmo, para cada passo, calcula o custo da posição atual e o custo da próxima posição(vizinhos) e escolhe seguir aquela na qual o custo é diminui mais, até chegar a um ponto onde nenhum vizinho melhora a solução (um mínimo local). Chama-se descida da colina exatamente por priorizar a redução do custo a cada iteração. A posição inicial escolhida é geralmente aleatória ou heurística.

As limitações do método dão-se pelo fato de ser um algoritmo ingênuo. Seguir sempre os mínimos locais não garante chegar ao mínimo global. O método pode ficar preso em pontos mínimos locais(ótimos locais), na qual precisaria mudar para uma posição que aumentaria o custo para que possa sair da situação e, possivelmente, encontrar o ótimo global, o que não acontece, uma vez que, por definição, o algoritmo não escolherá vizinhos que aumentem o custo. 
Também tem dificuldades ao lidar com planaltos(regiões onde todos vizinhos têm o mesmo valor - algoritmo não sabe para onde ir). e ridges(ótimos globais que exigem movimentos não diretamente descendentes - o algoritmo trava porque não aceita pioras.).
Para domínios mais complexos, ou até mesmo adicionando-se obstáculos, ele não funciona mais, pois pode ficar preso em obstáculos, que representariam o ponto mínimo local.

Para mitigar essas limitações, pode-se fazer alterações no algoritmo, criando variações.
Por exemplo, pode-se usar do conceito de temperatura. No início do algoritmo, ela é maior, permitindo que soluções não ótimas sejam escolhidas com certa probabilidade, promovendo exploração. Com o passar das iterações, contudo, a temperatura vai diminuindo, fazendo com que o algoritmo volte a escolher os vizinhos nos quais os custos são menores - explotação
Na varição estocástica, posições seguintes podem ser escolhidas com uma certa probabilidade. A adição de um fator probabilístico permite que o algoritmo explore novas soluções de vez em quando, mas ainda foque em uma busca local.

# 4. Qual a diferença da Descida da Colina e a Descida da Colina Estocástica?
Descida da Colina - Sempre aceita somente a próxima posição na qual o custo é o menor dentre as opções
Descida da Colina Estocástica - Posições seguintes podem ser escolhidas com uma certa probabilidade. Assim, posições que não diminuam o custo têm a chance de serem escolhidas, promovendo exploração de soluções

# 5. O que são métodos de otimização? Cite 3 deles.
São métodos/algoritmos que buscam minimizar(ou maximizar) uma função de custo, essencialmente buscando escolher a melhor dentre diversas soluções possíveis.
Ex.: ACO(Ant Colony Optimization), PSO(Particle Swarm Optimization) e Hillclimbing

# 6. Descreva como funciona (detalhadamente) o algoritmo enxame de partículas. Mostre (mesmo que em pseudocódigo) a fórmula de atualização de velocidade e explique-a.

O algoritmo começa com a criação de diversas partículas(soluções) iniciais, com posições e velocidades aleatórias. Em seguida, para cada iteração, a partícula muda para outra posição e a guarda se está for a melhor posição em que já esteve(baseando-se na função de cálculo de custo). Cada partícula recebe também a informação de qual é a melhor posição obtida dentre todas as partículas. A determinação de qual será a próxima posição depende da fórmula:

vᵢ(t+1) = W.vᵢ(t) + c₁ ⊙ [xᵢ*(t) − xᵢ(t)] + c₂ ⊙ [x_opt(t) − xᵢ(t)]

W representa a inércia - quanta influência a velocidade atual tem na velocidade seguinte

c1 - coeficiente congitivo: ajusta quanta influência a melhor posição individual(pbest) têm na velocidade

c2 - coeficiente social: ajusta quanta influência a melhor posição global(gbest) têm na velocidade

[xᵢ*(t) − xᵢ(t)] - vetor que aponta na direção do pbest -> magnitude muda de acordo com c1

[x_opt(t) − xᵢ(t)] - vetor que aponta na direção do gbest -> magnitude muda de acordo com c2
