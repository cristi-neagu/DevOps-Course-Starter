class ViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items

    @property
    def doingItems(self):
        return [item for item in self._items if item.status == 'Doing']

    @property
    def doneItems(self):
        return [item for item in self._items if item.status == 'Done']
    
    @property
    def toDoItems(self):
        return [item for item in self._items if item.status == 'To-Do']