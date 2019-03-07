import csv 

# temp definition
dictionary = []

def readCsv(filename) :

    csvmat = []

    with open(filename, newline='') as csvfile :

        data = csv.reader(csvfile, delimiter = '\t')

        for row in data :

            if len(row) > 0 :
                #print(row)
                csvmat.append(row)

    return csvmat

def readRules(filename) :

    with open(filename) as f :

        ruleDict = eval(f.read())

    #print(ruleDict)
    return ruleDict

def prettyOutput(nerList) :

    f = open("taggedNERs.csv","w+")

    wObj = csv.writer(f, delimiter="\t")

    docId = "NETTIK"

    randomInitial = "A"

    wMat = []

    numPerLine = 1

    for ner in nerList :
        wMat = []
        wMat.append(docId)

        wMat.append(randomInitial + ":"+str(ner['startIndex']) + ":" + str(ner['endIndex']))

        wMat.append(str(numPerLine))
        numPerLine += 1

        wMat.append(ner['name'])

        wObj.writerow(wMat)

    f.close()

def ifWindowIsThere(corpus, start, level, rule) :

    retval = 1

    for i in range(len(rule)) :

        if corpus[start + i][level] != rule[i] :

            retval = 0
            break

    return retval


def runRule(corpus, rule, level, howFar, chunkSize) :

    nerList = []

    # dividing the corpus in chunks of chunkSize
    start, end = 0, chunkSize - 1
    corpusLen = len(corpus)

    rule = eval(rule)

    while(end < corpusLen) :

        if ifWindowIsThere(corpus, start, level, rule) :

            startIndex = start + howFar

            # going through possible end-indices using window

            endIndex = end
            ner = {'name':""}
            while endIndex > startIndex :
                if isNER(endIndex, corpus[endIndex][level], corpus, dictionary) :
                    for i in range(startIndex, endIndex+1) :
                        ner['name'] += corpus[i][0] 
                        # to append or not to append a space?
                        if corpus[i][1] == "1" :
                            ner['name'] += " "
                    ner['startIndex'] = startIndex
                    ner['endIndex'] = endIndex
                    nerList.append(ner)
                    break
                else :
                    endIndex -= 1

        start += 1
        end += 1


    return nerList

def fitsRule(index, corpus) :
    return 0

def isNER(index, thing, corpus, dictionary) :

    if thing in dictionary :
        return 1
    elif not thing.isalpha() :
        return 1
    elif fitsRule(index, corpus) :
        return 1
    else :
        return 0

if __name__ == '__main__' :

    ruleSet = readRules('ruleFile.txt')

    corpus = readCsv('test.csv')

    nerSet = []

    for rule in ruleSet :
        print(rule)
        smolNerSet = runRule(corpus, rule, 2, ruleSet[rule], 7)

        nerSet += smolNerSet

    prettyOutput(nerSet)
