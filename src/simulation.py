from termooosolver import func_simulate, read_list_words, calculate_some_entropy, solve_nueto, Jogo

def simulate_termo(todas_palavras, simulated_words, solver):
    ocorrencias = [0, 0, 0, 0, 0, 0, 0]
    nao_conseguiu = []
    for i in simulated_words:
        print("A palavra que estou tentando acertar é: " + i)
        tentativas = solver(todas_palavras, func_simulate, [i], Jogo(1, 6))
        ocorrencias[tentativas - 1] += 1
        if tentativas == 0:
            nao_conseguiu.append(i)

    print("Número de vezes que acertei com 1 tentativa: " + str(ocorrencias[0]))
    print("Número de vezes que acertei com 2 tentativa: " + str(ocorrencias[1]))
    print("Número de vezes que acertei com 3 tentativa: " + str(ocorrencias[2]))
    print("Número de vezes que acertei com 4 tentativa: " + str(ocorrencias[3]))
    print("Número de vezes que acertei com 5 tentativa: " + str(ocorrencias[4]))
    print("Número de vezes que acertei com 6 tentativa: " + str(ocorrencias[5]))
    print("Número de vezes que não acertei : " + str(ocorrencias[6]))
    print(nao_conseguiu)

    return

def run_simulation_termo():
    lista = read_list_words('./data/WordList5Letter.txt')
    lista.sort(key=lambda x: x[1], reverse=True)
    lista_simulate = [ ]
    for i in lista:
        lista_simulate.append(i[0])

    lista = calculate_some_entropy(lista, lista)
    lista = list(dict.fromkeys(lista))
    simulate_termo(lista, lista_simulate, solve_nueto)

    return

if __name__ == '__main__':
    run_simulation_termo()