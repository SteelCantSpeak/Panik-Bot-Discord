import random

def GetSuccess(message):
    x = message.split()
    successes = 0
    rolls = int(x[1])
    results = "Rolling "+ str(rolls) + "d6 dice!\n"
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

    return["Rolling " + str(rolls) +"d6!", results, str(successes) + " successes"]
