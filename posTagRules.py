import sys

def howManyRulesCanWeMake(corpus, function, chunkSize, numOfRules) :

      totalMatches, totalFalsePos = 0

      matches = 0
      falsePos = sys.maxsize

      # derive like =n= rules
      ruleList = frameRules(numOfRules, corpus, function)

      # which rule (by index) being considered
      j = 0
      while j < len(ruleList) : 

            rule = ruleList[j]

            newMatches, newFalsePos = testRule(rule)
            judgement = judgeRule(newMatches, newFalsePos, matches, falsePos)


            if judgement == 0 :
                  allOurRules.append(rule)
                  totalMatches += newMatches
                  totalFalsePos += newFalsePos
                  j += 1
              elif judgement == 1 :
                  ruleList[j] = expandSieve(rule)
              elif judgement == -1 :
                  j += 1

      return ruleList, totalMatches, totalFalsePos



def posTagRules(corpus, function, chunkSize, numOfRules) :

      # final list of rules
      allOurRules = []


      # checking out how many rules we can make
      # that still make sense
      totalMatches, totalFalsePos = 0

      for i in range(numOfRules) :

          rules, newTotalMatches, newTotalFalsePos = howManyRulesCanWeMake(corpus, function, chunkSize, i)

          judgement = judgeRule(newTotalMatches, newTotalFalsePos, totalMatches, totalFalsePos)

          if judgement == 0 :
                allOurRules = rules
                totalMatches = newTotalMatches
                totalFalsePos = newTotalFalsePos

      return allOurRules
