class Human:

    # Human attributes
    fullName = ""
    id = ""
    age = 0
    height = 0
    weight = 0

    # human functions
    # full initialize
    def __init__(self,fullName, id, age, height, weight):
        self.fullName = fullName
        self.id = id
        self.age = age
        self.height = height
        self.weight = weight

    # print function
    def __str__(self):
        return ("name = " + self.fullName + ", id = " + self.id +
                ", age = " + self.age + ", height = " + self.height +
                ", weight = " + self.weight)

    # set methods
    # update new height (in case a child has grown or an elderly person has shrunk)
    def updateH(self, newHeight):
        self.height = newHeight

    # update new weight
    def updateW(self, newWeight):
        self.weight = newWeight

    # update age (person has aged)
    def updateA(self, newAge):
        self.age = newAge
