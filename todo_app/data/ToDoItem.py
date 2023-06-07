class TDItem:
    def __init__(self, itemID, name, status = 'To Do'):
        self.id = itemID
        self.name = name
        self.status = status

    @classmethod
    def fromTrelloCards(cls, card, cList):
        """
        Creates a new TDItem from Trello cards
        
        Args:
            card : Parsed json card from Trello API reqest
            cList: Parsed json list from Trello API request

        Returns:
            TDItem: New To Do item card
        """
        return cls(card['idShort'], card['name'], cList['name'])
