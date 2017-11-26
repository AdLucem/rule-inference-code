def windowFreq(windowList) :

    wFreq = {}

    for i in range(len(windowList)) :

        hashList = str(windowList[i])

        if hashList in wFreq :
            wFreq[hashList] += 1

        else :
            wFreq[hashList] = 1

    sortedWindows = []

    for j in sorted(wFreq,key=wFreq.get) :
        sortedWindows.append(eval(j))

    return sortedWindows

def frameRule(numRules, data, function) :

    for i in range(0,numRules) :

        rules[str(data[i])] = {'ruleFunction':function,'numId':0,'falsePos'=0}

    return rules

def runRule(corpusMatrix, rule) :

    # this is an extremely hacked-together function
    # that just checks for NER starting indices
    # and returns ALL the NNs after them
    # i'll write the generalised function later

    pass

def testRule(corpusList, corpusLevel, rule) :



if __name__ == '__main__' :

    l = eval(input())
    windowFreq(l)
