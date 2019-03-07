def readRules(filename) :

    with open(filename) as f :

        ruleDict = eval(f.read())

    print(ruleDict)
    return ruleDict
