import sys
import os
import csv

from posTagRules import posTagRules

def readCsv(filename) :

    csvmat = []

    with open(filename, newline='') as csvfile :

        data = csv.reader(csvfile, delimiter = '\t')

        for row in data :

            if len(row) > 0 :
                #print(row)
                csvmat.append(row)

    return csvmat


def readNer(filename) :

    mat = readCsv(filename)

    nerMat = []

    for row in mat :
        nerMat.append(row[4].split(' '))

    return nerMat

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

    sortedWindows.reverse()

    return sortedWindows

def frameRule(numRules, data) :

    rules = []

    for i in range(0,numRules) :

        rules.append(str(data[i]))

    return rules

def ifWindowIsThere(corpus, start, level, ruleStr) :

    retval = 1

    for i in range(len(ruleStr)) :

        if corpus[start + i][level] != ruleStr[i] :

            retval = 0
            break

    return retval


def testRule(rule, level, howFar) :

    matches, falsePos = 0, 0

    rule = eval(rule)
    corpus = readCsv('corpus.csv')

    # dividing the corpus in chunks of chunkSize
    start = 0
    corpusLen = len(corpus)

    while(start < corpusLen) :

        if ifWindowIsThere(corpus, start, level, rule) :

            # check if an NER starts this far away from window
            if corpus[start + (len(rule)-1) + howFar][2] == "1" :
                # success! match
                matches += 1

            # else if false positive
            else :
                falsePos = 0

        start += 1

    return matches, falsePos

def judgeRule(matches, falsePos, oldMatches, oldFalsePos, eps) :

    if (falsePos <= oldFalsePos) :

        # if it's reached a limit
        if (oldFalsePos - falsePos) < eps :
            if falsePos < matches/3 :
                # keep rule as-is
                return 1
            else :
                # junk rule
                return -1
        else :
            # yes, expand sieve
            return 0

    elif (falsePos > oldFalsePos) :
        return 2

def expandSieve(rule, corpus, level) :

    # search for most-frequently-occuring things
    # BEFORE rule

    start = 1
    lenCorp = len(corpus)

    freq = {}

    rule = eval(rule)

    while start < lenCorp :

        if ifWindowIsThere(corpus, start, level, rule) :
            if corpus[start-1][level] in freq.keys() :
                freq[corpus[start-1][level]] += 1
            else :
                freq[corpus[start-1][level]] = 1
        start += 1

    newrule = []

    for j in sorted(freq,key=freq.get) :
        if j == 0 :
            newrule.append(j)
            break
    newrule.extend(rule)
    return newrule

def parameters(start, size, howFar) :

    f = open("Params.hs","w+")

    f.write("module Params where\n\n")
    f.write("start :: Int\nstart = "+str(start)+"\n\n")
    f.write("size :: Int\nstart = "+str(size)+"\n\n")
    f.write("howFar :: Int\nstart = "+str(howFar)+"\n\n")

    f.close()

def mkRuleDict(rules, offset) :

    ruleDict = {}

    for rule in rules :
        if rule != None :
           ruleDict[str(rule)] = offset

    return ruleDict


def rule_inf_engine() :

    offset = 0
    n = 3
    startPos = 2

    corpus = readCsv('corpus.csv')
    parameters(startPos, n, offset)
    os.system("stack runghc incrRules.hs > windowList.txt")

    f = open("windowList.txt")
    windows = eval(f.read())
    f.close()
    data = windowFreq(windows)

    rules = frameRule(5, data)

    matches = 0
    falsePos = sys.maxsize
    i = 0
    times = 0

    while i < len(rules) :

      if times >= 5:
          i += 1
          continue

      rule = rules[i]

      newMatches, newFalsePos = testRule(rule, 1, 0)
      judgement = judgeRule(newMatches, newFalsePos, matches, falsePos, 5)

      if judgement == 0:

          prevRule = rule
          rules[i] = expandSieve(rule, corpus, 1)
          times += 1

      elif judgement == 1 :
          times = 0
          i += 1

      elif judgement == -1 :
          rules[i] = None
          times = 0
          i += 1

      # finally, make dictionary of rules
      ruleDict = mkRuleDict(rules, offset)

      return ruleDict



if __name__ == '__main__' :
    print(rule_inf_engine())
