def indexes():
    f = open("images-en-es/wikipedia.images.indexes")
    m = dict()

    for line in f:
        sep = line.index("|||")
        m[line[:sep]] = line[sep+3:-1]

    return m