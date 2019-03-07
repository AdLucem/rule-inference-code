import csv

def readCsv(filename) :

    csvmat = []

    with open(filename, newline='') as csvfile :

        data = csv.reader(csvfile, delimiter = '\t')

        for row in data :

            if len(row) > 0 :
                # print(row)
                csvmat.append(row)

    return csvmat

def hsCodeGen(mat) :

    f = open('Corpus.hs','w+')

    f.write('module Corpus where\n\n')
    f.write('import Types\n\n')
    f.write('corpusList :: [Token]\n')
    f.write('corpusList = [')

    for i in range(len(mat)) :

        row = mat[i]

        print(row)
        if i > 0 :
            f.write('  ')

        f.write('Token ')
        f.write('"' + row[0].lstrip('"').rstrip('"') + '" ')
        f.write('"' + row[1] + '" ')

        if row[2] == '0' :
            f.write("False")
        elif row[2] == '1' :
            f.write("True")

        if i < (len(mat) - 1) :
            f.write(',\n')

    f.write("]")
    f.close()

if __name__ == '__main__' :

    hsCodeGen(readCsv('corpus.csv'))
