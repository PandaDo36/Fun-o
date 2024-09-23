import random

# Função para criar um cromossomo aleatório
def criar_cromossomo(tamanho):
    return [random.randint(0, 1) for _ in range(tamanho)]

# Função para inicializar a população
def inicializar_populacao(numero_de_cromossomos, tamanho_cromossomo):
    return [criar_cromossomo(tamanho_cromossomo) for _ in range(numero_de_cromossomos)]

# Função para calcular o valor e peso de um cromossomo
def calcular_fitness(cromossomo, pesos_e_valores, peso_maximo):
    valor_total = 0
    peso_total = 0
    for i, gene in enumerate(cromossomo):
        if gene == 1:
            peso_total += pesos_e_valores[i][0]
            valor_total += pesos_e_valores[i][1]
    
    # Se o peso total exceder o máximo, o valor do fitness será 0
    if peso_total > peso_maximo:
        return 0
    return valor_total

# Função para avaliar a aptidão de toda a população
def avaliar_populacao(populacao, pesos_e_valores, peso_maximo):
    return [calcular_fitness(cromossomo, pesos_e_valores, peso_maximo) for cromossomo in populacao]

# Função de seleção por torneio
def torneio(populacao, aptidao, tamanho_torneio=3):
    selecionados = []
    for _ in range(len(populacao)):
        torneio = random.sample(list(zip(populacao, aptidao)), tamanho_torneio)
        vencedor = max(torneio, key=lambda x: x[1])
        selecionados.append(vencedor[0])
    return selecionados

# Função para realizar o crossover entre dois pais
def crossover(pai1, pai2):
    ponto_de_corte = random.randint(1, len(pai1) - 1)
    filho1 = pai1[:ponto_de_corte] + pai2[ponto_de_corte:]
    filho2 = pai2[:ponto_de_corte] + pai1[ponto_de_corte:]
    return filho1, filho2

# Função para aplicar mutação em um cromossomo
def mutacao(cromossomo, taxa_mutacao=0.01):
    for i in range(len(cromossomo)):
        if random.random() < taxa_mutacao:
            cromossomo[i] = 1 - cromossomo[i]  
    return cromossomo

# Função de elitismo (preserva o melhor indivíduo)
def aplicar_elitismo(populacao, aptidao, nova_populacao):
    melhor_indice = aptidao.index(max(aptidao))
    melhor_individuo = populacao[melhor_indice]
    nova_populacao[random.randint(0, len(nova_populacao)-1)] = melhor_individuo
    return nova_populacao

# Função principal do algoritmo genético
def mochila_genetica(pesos_e_valores, peso_maximo, numero_de_cromossomos, geracoes, taxa_mutacao=0.01, usar_elitismo=True):
    tamanho_cromossomo = len(pesos_e_valores)
    populacao = inicializar_populacao(numero_de_cromossomos, tamanho_cromossomo)
    lista_melhores = []
    
    for geracao in range(geracoes):
        aptidao = avaliar_populacao(populacao, pesos_e_valores, peso_maximo)
        pais = torneio(populacao, aptidao)
        
        nova_populacao = []
        for i in range(0, len(pais), 2):
            pai1, pai2 = pais[i], pais[i+1]
            filho1, filho2 = crossover(pai1, pai2)
            nova_populacao.append(mutacao(filho1, taxa_mutacao))
            nova_populacao.append(mutacao(filho2, taxa_mutacao))
        
        if usar_elitismo:
            nova_populacao = aplicar_elitismo(populacao, aptidao, nova_populacao)
        
        populacao = nova_populacao
        melhor_aptidao = max(aptidao)
        melhor_individuo = populacao[aptidao.index(melhor_aptidao)]
        lista_melhores.append([melhor_aptidao, melhor_individuo])
    
    return lista_melhores

# Exemplo de uso
pesos_e_valores = [[2, 10], [4, 30], [6, 300], [8, 10], [8, 30], [8, 300], [12, 50], [25, 75], [50, 100], [100, 400]]
peso_maximo = 100
numero_de_cromossomos = 150
geracoes = 50

resultado = mochila_genetica(pesos_e_valores, peso_maximo, numero_de_cromossomos, geracoes)
for geracao, melhor in enumerate(resultado):
    print(f"Geração {geracao+1}: Melhor valor = {melhor[0]}, Cromossomo = {melhor[1]}")
