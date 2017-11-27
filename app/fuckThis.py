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

    import sys

    l = eval(input())

    # final list of rules
    allOurRules = []

    # context window size
    for i in range(4,10) :

        totalMatches = 0
        totalFalsePos = 0
        matches = 0
        falsePos = sys.maxsize

        # number of rules
        for j in range(1,10) :

            rule = frameRule()
            newMatches, newFalsePos = testRule(rule)
            judgement = judgeRule(newMatches, newFalsePos, matches, falsePos)

            if judgement == 0 :
                allOurRules.append(rule)
            elif judgement == 1 :
                expandSieve(rule)
            elif judgement == -1 :
                continue
