import random


class Guess:
    def __init__(self):
        self.value = "{:02d}".format(random.randrange(0, 99))
        self.playerValue = None
        self.currentScore = 0.0
    
    def setPlayerValue(self, value):
        self.playerValue = value

    def getPlayerValue(self):
        return self.playerValue or 'Загадано:'
        
    def setScore(self, score):
        self.currentScore = score

    def getScore(self):
        return self.currentScore

    def getValue(self):
        return self.value

    def getResult(self):
        return self.playerValue == self.value


class Psychic:
    def __init__(self, name):
        self.name = name
        self.history = []
        
    def getName(self):
        return self.name

    def getScore(self):
        if len(self.history) == 0:
            return 0
        return self.history[0].getScore()
    
    def calcScore(self):
        c = 0
        for g in self.history:
            c += int(g.getResult())
        if len(self.history) > 0:
            self.history[0].setScore(c * 100.0 / len(self.history))

    def setPlayerValue(self, value):
        if not len(self.history):
            return None
        self.history[0].setPlayerValue(value)
        self.calcScore()

    def getGuess(self, index):
        if index >= len(self.history):
            return None
        return self.history[index]
    
    def addGuess(self):
        self.history.insert(0, Guess())
