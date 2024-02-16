import cProfile
from math import log
import numpy as np
from collections import Counter
from dictWords import intToWord, wordToInt


# Da a lista de palavras de um arquivo
def read_list_words(path):
    lista_palavras = []
    f = open(path, encoding="utf8")
    for i in f:
        i = (i.rstrip('\n')).lower()
        valor = 0
        lista_palavras.append((i, valor))
    return lista_palavras

# Dado uma letra e a ocorrencia de amarelos dela, remove todos as ocorrencias das que nao seguem o padrao
def remove_yellow(lista_palavras, letra, ocorrencias, pos, mode= None):
    i = 0
    count = 0
    while i < len(lista_palavras):
        if letra == lista_palavras[i][0][pos]:
            if mode == None:
                lista_palavras.pop(i)
            i -= 1
            count += 1
        i += 1
    
    i = 0
    while i < len(lista_palavras):
        ocorrencias_pal = 0
        for j in range(0, 5):
            if lista_palavras[i][0][j] == letra:
                ocorrencias_pal += 1
        if ocorrencias_pal < ocorrencias:
            if mode == None:
                lista_palavras.pop(i)
            i -= 1
            count += 1
        i += 1

# Remove as palavras sem aquela letra na posicao
def remove_green(lista_palavras, letra, posicao):
    count = 0
    i = 0
    while i < len(lista_palavras):
        if letra != lista_palavras[i][0][posicao]:
            
            lista_palavras.pop(i)
            i -= 1
            count += 1
        i += 1

# Remove as palavras com essa letra
def remove_black(lista_palavras, letra):
    count = 0
    i = 0
    while i < len(lista_palavras):
        if letra in lista_palavras[i][0]:
            
            lista_palavras.pop(i)
            i -= 1
            count += 1
        i += 1
    return count

def func_usuario(new_word, target):
    return input("Entre o resultado da palavra passada (P = Preto, A = Amarelo, V = Verde), na forma X X X X X\n").split(" ")

# Dado uma palavra nova e um target, calcula qual o resultado deveria ser
def func_simulate(new_word, target):
    new_word = list(new_word)
    target = list(target)
    result = ['', '', '', '', '']
    # Primeiro vamos ver se tem um verde
    for i in range(0, 5):
        if new_word[i] == target[i]:
            result[i] = 'V'
            target[i] = '-'
            new_word[i] = '-'
    
    i = 0
    for i in range(0, 5):
        if new_word[i] != '-' and new_word[i] in target:
            result[i] = 'A'
            target[target.index(new_word[i])] = '-'
            new_word[i] = '-'
        elif new_word[i] != '-':
            result[i] = 'P'

    
    return (result)

# Remove 
def remove_duplicates(lista_palavras, letra, ocorrencia):
    i = 0
    while i < len(lista_palavras):
        if lista_palavras[i][0].count(letra) >= ocorrencia:
            lista_palavras.pop(i)
            i -= 1
        i += 1
    return

def remove_not_there(lista_palavras, letra, posicoes):
    i = 0
    for j in posicoes:
        while i < len(lista_palavras):
            A = lista_palavras[i][0][j]
            if lista_palavras[i][0][j] == letra:
                lista_palavras.pop(i)
                i -= 1
            i += 1
    return

def remove_letter_ocorrencies(lista_palavras, letra, ocorrencias):
    i = 0
    while i < len(lista_palavras):
        if lista_palavras[i][0].count(letra) < ocorrencias:
            lista_palavras.pop(i)
            i -= 1
        i += 1
    return

# Remove as palavras que nao sao mais possiveis como resposta
def remove_impossible(lista_palavras, pretos, amarelos, verdes):
    # Se o preto também é amarelo ou verde, nao podemos tira-los
    duplicates = {}
    not_there = {}
    ocorrencias = {}

    for i in pretos:
        not_there[i] = []

    for j in amarelos:
        if ocorrencias.get(j) != None:
            ocorrencias[j] += 1
        else:
            ocorrencias[j] = 1

    for j in verdes:
        if ocorrencias.get(j) != None:
            ocorrencias[j] += 1
        else:
            ocorrencias[j] = 1

    j = 0
    while j < len(pretos):
        if amarelos.get(pretos[j][0]) != None or verdes.get(pretos[j][0]) != None:
            # Esse if ta meio estranho, mas nao quero demorar muito pra terminar D:
            if amarelos.get(pretos[j][0]) != None and duplicates.get(pretos[j][0]) == None:
                duplicates[pretos[j][0]] = len(amarelos[pretos[j][0]])

            elif verdes.get(pretos[j][0]) != None and duplicates.get(pretos[j][0]) == None:\
                duplicates[pretos[j][0]] = len(verdes[pretos[j][0]]) + 1

            elif amarelos.get(pretos[j][0]) != None and duplicates.get(pretos[j][0]) != None:
                duplicates[pretos[j][0]] += len(amarelos[pretos[j][0]]) - 1
            else:
                duplicates[pretos[j][0]] += len(verdes[pretos[j][0]])
            not_there[pretos[j]].append(pretos[j][1])    
            pretos.pop(j)
            j -= 1  
        j += 1

    for j in not_there:
        remove_not_there(lista_palavras, j[0], not_there[j])

    for j in duplicates:
        remove_duplicates(lista_palavras, j, duplicates[j])

    for j in ocorrencias:
        remove_letter_ocorrencies(lista_palavras, j, ocorrencias[j])

    # Remove o que deveriamos remover
    for j in pretos:
        remove_black(lista_palavras, j[0])
    
    for j in verdes:
        for k in verdes[j]:
            remove_green(lista_palavras, j, k)

    for j in amarelos:
        for k in range(1, len(amarelos[j])):
            remove_yellow(lista_palavras, j, amarelos[j][0], amarelos[j][k])
    
    return lista_palavras

# Calcula a entropia pra todas as palavras da wordlist
def calculate_all_entropy(wordlist):
    resp = []
    size = len(wordlist)
    f = open("./lookUpMatrix.npy", mode='rb')
    # Vai pra linha do arquivo que quero
    matrix = np.load(f)

    i = 0
    for linha in matrix:
        vet_ocorrencias = np.zeros(3**5, dtype=int)
        # Aqui uns 9
        
        unique, counts = np.unique(linha, return_counts=True)
        contado = dict(zip(unique, counts))

        for k in contado:
            vet_ocorrencias[int(k)] = contado[k]

        entropy = 0

        # Aqui gasta 7 sec
        def calc_entropy(t):
            if t != 0:
                return t / size * log(size / t, 2)
            else:
                return 0

        vfunc = np.vectorize(calc_entropy, otypes=[np.float32])
        result = vfunc(vet_ocorrencias)
        entropy = sum(result)

        resp.append((intToWord[i], entropy))
        i += 1
    f.close()
    resp.sort(key=lambda x: x[1], reverse=True)
    return resp

# Calcula a entropia de algumas palavras que ainda sao possiveis?
def calculate_some_entropy(wordlist, allwords):
    resp = []
    size = len(wordlist)
    f = open("./lookUpMatrix.npy", mode='rb')
    # Vai pra linha do arquivo que quero
    matrix = np.load(f)

    def calc_entropy(t):
        if t != 0:
            return t / size * log(size / t, 2)
        else:
            return 0

    vfunc = np.vectorize(calc_entropy, otypes=[np.float32])

    indices = []
    for i in wordlist:
        indices.append(wordToInt[i[0]])

    matrix = matrix[:, indices]

    for i in allwords:
        vet_ocorrencias = np.zeros(3**5, dtype=np.float32)
        linha = matrix[wordToInt[i[0]]]
        
        unique, counts = np.unique(linha, return_counts=True)
        contado = dict(zip(unique, counts))

        for k in contado:
            vet_ocorrencias[int(k)] = contado[k]

        entropy = 0
        result = vfunc(vet_ocorrencias)
        entropy = sum(result)  

        resp.append((i[0], entropy))

    resp.sort(key=lambda x: x[1], reverse=True)
    return resp

# Dado uma configuracao, associa um numero pra ela, usando a ideia de um numero na base 3.
# Para isso vamos usar o codigo 0 = Preto, 1 = Amarelo, 2 = Verde.
def decode_pos(configuracao):
    cont = 0
    resp = 0
    for i in configuracao:
        if i == "A":
            resp += 3**(4 - cont)
        elif i == "V":
            resp += 3**(4 - cont) * 2
        cont += 1
    return resp

# Solver simples de termo
def solve_termo(lista_palavras, func_res, target):
    new_lista = []

    for i in lista_palavras:
        new_lista.append(i)

    allwords = lista_palavras
    lista_palavras = new_lista

    num_tentativas = -1
    print("A primeira palavra é:" + lista_palavras[0][0])
    palavra_passada = allwords[0][0]
    for i in range(0, 6):
        resultado = func_res(palavra_passada, target)
        # Aqui teria que verificar se o resultado ta formatado certo

        if resultado == ['V', 'V', 'V', 'V', 'V']:
            num_tentativas = i
            break

        # Calcula os verdes, com uma lista de posicoes, os pretos + posicao e os amarelos com a frequencia + posicao
        verdes, amarelos, pretos = {}, {}, []

        for j in range(0, 5):
            if resultado[j] == 'A':
                if amarelos.get(palavra_passada[j]) == None:
                    amarelos[palavra_passada[j]] = [1, j]
                else:
                    amarelos[palavra_passada[j]][0] += 1
                    amarelos[palavra_passada[j]].append(j)
            elif resultado[j] == 'P':
                pretos.append((palavra_passada[j], j))
            else:
                if verdes.get(palavra_passada[j]) == None:
                    verdes[palavra_passada[j]] = [j]
                else:
                    verdes[palavra_passada[j]].append(j)
        
        j = 0
        
        # Tem problema na funcao abaixo :(
        remove_impossible(lista_palavras, pretos, amarelos, verdes)
        allwords = calculate_some_entropy(lista_palavras, allwords)


        if len(lista_palavras) > 2:
            palavra_passada = allwords[0][0]

        else:
            palavra_passada = lista_palavras[0][0]
        
        print("A proxima palavra é " + palavra_passada)

    if num_tentativas != -1:
        print("Foram " + str(num_tentativas + 1) + " tentativas.")
    else:
        print("Não consegui acertar")

    return num_tentativas + 1

def simulate(todas_palavras, simulated_words, solver):
    ocorrencias = [0, 0, 0, 0, 0, 0, 0]
    nao_conseguiu = []
    for i in simulated_words:
        print("A palavra que estou tentando acertar é: " + i)
        tentativas = solver(todas_palavras, func_simulate, i)
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

lista = read_list_words('./WordList5Letter.txt')
lista.sort(key=lambda x: x[1], reverse=True)
lista_simulate = ["capaz", "velho", 'conto']
b = 'arroz'.count("r")

#lista = calculate_all_entropy(lista)
#lista.sort(key=lambda x: x[1], reverse=True)

#lista_simulate = []

for i in lista:
    lista_simulate.append(i[0])

lista = calculate_all_entropy(lista)

lista = list(dict.fromkeys(lista))
solve_termo(lista, func_usuario, None) 
#simulate(lista, lista_simulate, solve_termo)
    
#cProfile.run('calculate_all_entropy(lista)')
#cProfile.run('calculate_some_entropy(lista[:50], lista)')
#calculate_all_entropy(lista)
    