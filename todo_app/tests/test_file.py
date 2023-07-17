import pytest
from todo_app.data.ViewModel import ViewModel
from todo_app.data.ToDoItem import TDItem

def test_doing():
    testItems = [
        TDItem(1, '1st item', 'Doing'),
        TDItem(2, '2nd item', 'Doing'),
        TDItem(3, '3rd item', 'To-Do'),
        TDItem(4, '4th item', 'Doing'),
        TDItem(5, '5th item', 'Done'),
        TDItem(6, '6th item', 'Doing'),
        ]

    itemModel = ViewModel(testItems)

    assert len(itemModel.doingItems) == 4
