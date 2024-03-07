import cProfile
from math import log
import numpy as np
from collections import Counter
from dictWords import intToWord, wordToInt

class Jogo:
    def __init__(self, palavras, tentativas):
        self.palavras = palavras
        self.tentativas = tentativas
        

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
    entrada = input("Entre o resultado da palavra passada (P = Preto, A = Amarelo, V = Verde), na forma X X X X X\n").split(" ")
    resp = []
    resp.append(entrada)
    return resp

# Dado uma palavra nova e um target, calcula qual o resultado deveria ser
def func_simulate(word, targets):
    resp = []
    for k in range(0, len(targets)):
        # Primeiro vamos ver se tem um verde
        new_target = list(targets[k])
        new_word = list(word)
        result = ['', '', '', '', '']
        for i in range(0, 5):
            if new_word[i] == new_target[i]:
                result[i] = 'V'
                new_target[i] = '-'
                new_word[i] = '-' # Atauliza para marcar que aquele foi processado
        
        i = 0
        # Depois verifica os amarelos e os pretos
        for i in range(0, 5):
            if new_word[i] != '-' and new_word[i] in new_target:
                result[i] = 'A'
                new_target[new_target.index(new_word[i])] = '-'
                new_word[i] = '-'
            elif new_word[i] != '-':
                result[i] = 'P'
        
        resp.append(result)
    
    return (resp)

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
                duplicates[pretos[j][0]] = len(amarelos[pretos[j][0]]) + 1

            elif verdes.get(pretos[j][0]) != None and duplicates.get(pretos[j][0]) == None:
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

# Calcula a entropia de algumas palavras que ainda sao possiveis?
def calculate_some_entropy(wordlist, allwords):
    resp = []
    size = len(wordlist)
    f = open("./data/lookUpMatrix.npy", mode='rb')
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

def calculate_colors(resultado, palavra_passada):
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
    
    return verdes, amarelos, pretos

def merge_lists(list_of_lists):
    for i in list_of_lists:
        i.sort(key=lambda x: x[0])
    resp = list_of_lists[0].copy()

    for i in range(0, len(list_of_lists[0])):
        soma = 0
        for j in range(0, len(list_of_lists)):
            soma += list_of_lists[j][i][1]
        resp[i] = (resp[i][0], soma)

    return resp

def func_usuario_nueto(a, b):
    resp = input("De a resposta onde P = Preto, A = Amarelo, V = Verde, da forma PALAVRA | PALAVRA | ... ")
    resp = resp.split("|")
    final = []
    for i in resp:
        final.append(i.split(" "))
    for i in final:
        if "" in i:
            i.remove("")
    return final

def solve_nueto(lista_palavras, func_res, targets, tipo_jogo):
    list_of_lists_values = []
    list_of_lists_remaining = []
    nao_feitas = []
    # Cria duas listas de listas, uma que representa as palavras faltantes pra cada coluna
    # E outra pro valor de entropia pra cada coluna
    for i in range(0, tipo_jogo.palavras):
        list_of_lists_values.append([])
        list_of_lists_remaining.append([])
        nao_feitas.append(i)
        for j in lista_palavras:
            list_of_lists_values[i].append(j)
            list_of_lists_remaining[i].append(j)
    
    # Junta as listas somando o valor das entropias pra cada
    resp = merge_lists(list_of_lists_remaining)
    resp.sort(key=lambda x: x[1], reverse=True)

    num_tentativas = 0
    print("A proxima palavra é:" + str(resp[0][0]))
    palavra_passada = resp[0][0]
    pontos = 0


    for i in range(0, tipo_jogo.tentativas):
        resultado = func_res(palavra_passada, targets)
        j = 0
        tenho_remover = []
        for k in nao_feitas:
            # Verifica se acertei a palavra e remove a palavra
            if resultado[j] == ['V', 'V', 'V', 'V', 'V']:
                list_of_lists_remaining[k] = [(palavra_passada, 0), (palavra_passada, 0)]
                pontos += 1
                tenho_remover.append(k)

            # Calcula os dicionarios pra remover as que nao podem ser
            else:
                verde, amarelo, preto = calculate_colors(resultado[j], palavra_passada)
                remove_impossible(list_of_lists_remaining[k], preto, amarelo, verde)

            # Recalcula a entropia    
            list_of_lists_values[k] = calculate_some_entropy(list_of_lists_remaining[k], list_of_lists_values[k])
            j += 1

        # Remove as que eu tenho que remover (Eu to removendo aqui porque se nao criava um bug)
        for k in tenho_remover:
            nao_feitas.remove(k)

        # Junta as entropias e pega a palavra nova
        resp = merge_lists(list_of_lists_values)
        resp.sort(key=lambda x: x[1], reverse=True)
        palavra_passada = resp[0][0]


        # Verifica se ja tenho certeza de alguma palavra e chuta ela
        for i in list_of_lists_remaining:
            if len(i) == 1:
                palavra_passada = i[0][0]
                break

        if len(nao_feitas) == 1:
            for i in list_of_lists_remaining:
                if len(i) == 2:
                    palavra_passada = i[0][0]
                    break

        if pontos == tipo_jogo.palavras:
            num_tentativas += 1
            break

        num_tentativas += 1
        print("A proxima palavra é:" + str(palavra_passada))

    if len(nao_feitas) != 0:
        num_tentativas = 0
    print("Gastei " + str(num_tentativas) + " tentativas")
    
    return num_tentativas


if __name__ == '__main__':
    lista = read_list_words('./data/WordList5Letter.txt')
    lista.sort(key=lambda x: x[1], reverse=True)
    lista = calculate_some_entropy(lista, lista)
    lista = list(dict.fromkeys(lista))
    
    tipo_jogo = input("Entre o tipo de jogo(1 = termo, 2 = dueto, 4 = quarteto): ")

    # To com o python desatualizado
    if tipo_jogo == '1':
            jogo = Jogo(1, 6)
            func = func_usuario
    elif tipo_jogo == '2':
            jogo = Jogo(2, 7)
            func = func_usuario_nueto
    elif tipo_jogo == '4':
            jogo = Jogo(4, 9)
            func = func_usuario_nueto
    else:
            raise(SyntaxError)
        
    solve_nueto(lista, func, None, jogo)
