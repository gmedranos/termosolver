# Vamos cria um arquivo txt para guardar as configuracoes possiveis para cada palavra
# A ideia é que o arquivo tenha palavras nas linhas e coluna. Se eu estiver na linha "Palavra1" e na coluna "Palavra2"
# O que aparece deve ser o padrao que apareceria ao colocar a Palavra1 considerando que a Palavra 2 é a resposta
# Exemplo, se palavra1 = forte, palavra2 = carro, deveria aparecer o padrao "P A V P P".
# Para facilitar algumas coisas, vamos guardar o padrao como se fosse um numero na base 3, com P = 0,
# A = 1, V = 2.

from termooosolver import decode_pos, read_list_words, func_simulate
import numpy as np

# Cria um arquivo txt com as configuracoes
def create_file():
    wordlist = read_list_words("./data/WordList5Letter.txt")
    f = open("./data/configuracoes.txt", mode='w')
    f.write("     ")
    for i in wordlist:
        f.write(" " + i[0])
    f.write("\n")

    for i in wordlist:
        f.write(i[0])
        for j in wordlist:
            padrao = func_simulate(i[0], j[0])
            num = str(decode_pos(padrao))
            f.write(" " + num)
        f.write("\n")
    f.close()
    return

# Cria uma matriz de numpy com as configuracoes
def create_numpy_matrix():
    wordlist = read_list_words("./data/WordList5Letter.txt")
    f = open("./data/lookUpMatrix.npy", mode='wb')
    array = np.zeros((5482, 5482), dtype=np.uint8)
    x = 0
    for i in wordlist:
        y = 0
        for j in wordlist:
            lista_palavra = []
            lista_palavra.append(j[0])
            padrao = func_simulate(i[0], lista_palavra)
            num = decode_pos(padrao[0])
            array[x][y] = num
            y += 1
        x += 1
    print("oi")
    np.save(f, array)
    return

# Cria os dicionarios do dictWords.py
def create_dicts():
    wordlist = read_list_words("./data/WordList5Letter.txt")
    f = open("./src/dictWords.py", mode='w')
    f.write("# Vou guardar 2 dicionarios aqui, um que converte uma palavra pra uma posicao na matriz.")
    f.write("\n")
    f.write('# E um que pega uma posicao e retorna a palavra')
    f.write("\n\n\n")
    f.write('wordToInt = {')
    f.write("\n")

    i = 0
    while i < len(wordlist):
        dict_line = '           "' + wordlist[i][0] + '" : ' + str(i) + ','
        f.write(dict_line)
        f.write("\n")
        i += 1

    f.write("}")
    f.write("\n\n")

    f.write('intToWord = {')
    f.write("\n")
    i = 0
    while i < len(wordlist):
        dict_line = '           ' + str(i) + ' : "' + wordlist[i][0] + '",'
        f.write(dict_line)
        f.write("\n")
        i += 1

    f.write("}")
    f.close()
    return

#create_file()

#create_dicts()
create_numpy_matrix()