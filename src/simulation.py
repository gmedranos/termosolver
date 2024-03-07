from termooosolver import func_simulate, read_list_words, calculate_some_entropy, solve_nueto, Jogo
import random as r

def simulate_termo(todas_palavras, simulated_words, solver, mode):
    ocorrencias = [0, 0, 0, 0, 0, 0, 0]

    if mode == 2:
        for i in range(0, 1):
            ocorrencias.append(0)
    elif mode == 4:
        for i in range(0, 3):
            ocorrencias.append(0)

    nao_conseguiu = []
    for i in simulated_words:
        print("A palavra que estou tentando acertar é: " + str(i))
        jogo = ''
        if mode == 1:
            jogo = Jogo(1,6)
        elif mode == 2:
            jogo = Jogo(2, 7)
        else:
            jogo = Jogo(4, 9)

        tentativas = solver(todas_palavras, func_simulate, i, jogo)
        ocorrencias[tentativas - 1] += 1
        if tentativas == 0:
            nao_conseguiu.append(i)

    for i in range(0, len(ocorrencias) - 1):
        print("Número de vezes que acertei com " +  str(i + 1)  + " tentativas: " + str(ocorrencias[i]))    

    print("Número de vezes que não acertei : " + str(ocorrencias[-1]))
    print(nao_conseguiu)

    return

def run_simulation_termo():
    lista = read_list_words('./data/WordList5Letter.txt')
    lista.sort(key=lambda x: x[1], reverse=True)
    lista_simulate = [ ]
    for i in lista:
        lista_simulate.append([i[0]])

    lista = calculate_some_entropy(lista, lista)
    lista = list(dict.fromkeys(lista))
    simulate_termo(lista, lista_simulate, solve_nueto, 1)

    return

def run_simulation_dueto():
    lista = read_list_words('./data/WordList5Letter.txt')
    lista.sort(key=lambda x: x[1], reverse=True)


    lista_simulate = []
    for i in range(0, 10):
        ind_1, ind_2 = r.randrange(0, 5480), r.randrange(0, 5480)
        while ind_1 == ind_2:
            ind_2 = r.randrange(0, 5480)
        lista_simulate.append([lista[ind_1][0], lista[ind_2][0]])

    lista = calculate_some_entropy(lista, lista)
    lista = list(dict.fromkeys(lista))

    simulate_termo(lista, lista_simulate, solve_nueto, 2)

    return

def run_simulation_quarteto():
    lista = read_list_words('./data/WordList5Letter.txt')
    lista.sort(key=lambda x: x[1], reverse=True)
    lista_simulate = []
    for i in range(0, 2000):
        ind_1, ind_2 = r.randrange(0, 5480), r.randrange(0, 5480)
        while ind_1 == ind_2:
            ind_2 = r.randrange(0, 5480)
        ind_3 = r.randrange(0, 5480)
        
        while ind_1 == ind_3 or ind_2 == ind_3:
            ind_3 = r.randrange(0, 5480)

        ind_4 = r.randrange(0, 5480)

        while ind_1 == ind_4 or ind_2 == ind_4 or ind_3 == ind_4:
            r.randrange(0, 5480)

        lista_simulate.append([lista[ind_1][0], lista[ind_2][0], lista[ind_3][0], lista[ind_4][0]])

    lista = calculate_some_entropy(lista, lista)
    lista = list(dict.fromkeys(lista))

    simulate_termo(lista, lista_simulate, solve_nueto, 4)

    return

if __name__ == '__main__':
    run_simulation_dueto()