class IBBFObj:
    def __init__(self, identifier):
        if isinstance(identifier, str):
            self.identifier = []
            self.identifier.append(identifier)
        else:
            self.identifier = identifier

    def __hash__(self):
        return hash(''.join(self.identifier))

    def __eq__(self, other):

        if isinstance(other, str):
            return ''.join(self.identifier) == other
        else:
            return self.identifier == other

    def __ne__(self, other):
        #print("First:\t" + str(self))
        #print("Second:\t" + str(other))
        #return not (self == other)

        if isinstance(other, str):
            return ''.join(self.identifier) != other
        else:
            return self.identifier != other

    def __add__(self, other):
        return IBBFObj(self.identifier + other.identifier)

    def removeElement(self):
        tmp = list(self.identifier)
        tmp.pop()
        return IBBFObj(tmp)