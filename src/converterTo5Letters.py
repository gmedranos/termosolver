def convertWordsListTo5Letter():
    path_read = './data/WordList.txt'
    path_write = './data/WordList5Letter.txt'
    num_linhas = 261799

    read_file = open(path_read, encoding="utf8")
    write_file = open(path_write, 'w')

    for linha in read_file:
        if len(linha) == 6 and linha[5] == '\n':
            write_file.write(linha)
        elif len(linha) == 5 and linha[4] != '\n':
            write_file.write(linha)
    return

#convertWordsListTo5Letter()