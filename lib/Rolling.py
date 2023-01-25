import random

def GetSuccess(message):
  x = message.split()

  if "d" in x[1]:
    score = x[1]
    y = str(score).split("d")
    rolls = int(y[0])
    results = "Rolling "+ str(rolls) + "d6 dice!\n"
    return rollDice(results, rolls)
  else:
    rolls = int(x[1])
    results = "Rolling "+ str(rolls) + "d6 dice!\n"
    return rollDice(results, rolls)

def rollDice(header, rolls):
    successes = 0
    results = ""
    i = 1
        
    while i <= rolls:
        value = random.randint(1,6)
          
        if value % 2 == 0:
            successes += 1
            
        if value == 6:
            results += "**"+str(value)+"**"
            successes += 1 #Double points
        else:
            results += str(value)
        if i < rolls:
            results += ", "
        i+= 1

    return[header, results, str(successes) + " successes"]