class TDItem:
    def __init__(self, itemID, name, status = 'To Do'):
        self.id = itemID
        self.name = name
        self.status = status

    @classmethod
    def fromTrelloCards(cls, card, cList):
        return cls(card['idShort'], card['name'], cList['name'])
