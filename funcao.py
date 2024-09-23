import random

def binario_para_real(binario, intervalo):
    decimal = int("".join(map(str, binario)), 2)
    return intervalo[0] + (intervalo[1] - intervalo[0]) * decimal / (2**len(binario) - 1)

def inicializar_populacao_binaria(num_cromossomos, bits):
    return [[random.randint(0, 1) for _ in range(bits)] for _ in range(num_cromossomos)]

def funcao(x):
    return x**3 - 6*x + 14

def calcular_fitness(cromossomo, intervalo):
    x = binario_para_real(cromossomo, intervalo)
    return -funcao(x)

def avaliar_populacao(populacao, intervalo):
    return [calcular_fitness(cromossomo, intervalo) for cromossomo in populacao]

def torneio(populacao, aptidao, tamanho_torneio=3):
    return [max(random.sample(list(zip(populacao, aptidao)), tamanho_torneio), key=lambda x: x[1])[0] for _ in range(len(populacao))]

def crossover(pai1, pai2):
    ponto_de_corte = random.randint(1, len(pai1) - 1)
    return pai1[:ponto_de_corte] + pai2[ponto_de_corte:], pai2[:ponto_de_corte] + pai1[ponto_de_corte:]

def mutacao(cromossomo, taxa_mutacao=0.01):
    return [1 - gene if random.random() < taxa_mutacao else gene for gene in cromossomo]

def aplicar_elitismo(populacao, aptidao, nova_populacao):
    melhor_individuo = populacao[aptidao.index(max(aptidao))]
    nova_populacao[random.randint(0, len(nova_populacao)-1)] = melhor_individuo
    return nova_populacao

def minimizar_funcao(num_cromossomos, geracoes, taxa_mutacao=0.01, usar_elitismo=True):
    intervalo = [-10, 10]
    bits = 16
    populacao = inicializar_populacao_binaria(num_cromossomos, bits)
    lista_melhores = []
    
    for _ in range(geracoes):
        aptidao = avaliar_populacao(populacao, intervalo)
        pais = torneio(populacao, aptidao)
        
        nova_populacao = []
        for i in range(0, len(pais), 2):
            filho1, filho2 = crossover(pais[i], pais[i+1])
            nova_populacao.extend([mutacao(filho1, taxa_mutacao), mutacao(filho2, taxa_mutacao)])
        
        if usar_elitismo:
            nova_populacao = aplicar_elitismo(populacao, aptidao, nova_populacao)
        
        populacao = nova_populacao
        melhor_aptidao = max(aptidao)
        melhor_individuo = populacao[aptidao.index(melhor_aptidao)]
        lista_melhores.append([melhor_aptidao, melhor_individuo])
    
    return lista_melhores

# Exemplo de uso
num_cromossomos = 10
geracoes = 50
resultado = minimizar_funcao(num_cromossomos, geracoes)

for geracao, melhor in enumerate(resultado):
    x_melhor = binario_para_real(melhor[1], [-10, 10])
    print(f"Geração {geracao+1}: Valor de x = {x_melhor}, Valor da função = {-melhor[0]}")
