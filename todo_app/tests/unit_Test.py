import pytest
from todo_app.data.ViewModel import ViewModel
from todo_app.data.ToDoItem import TDItem

@pytest.fixture
def testItems():
    return [
        TDItem(1, '1st item', 'Doing'),
        TDItem(2, '2nd item', 'Doing'),
        TDItem(3, '3rd item', 'To-Do'),
        TDItem(4, '4th item', 'Doing'),
        TDItem(5, '5th item', 'Done'),
        TDItem(6, '6th item', 'Doing'),
        TDItem(7, '7th item', 'Done'),
        TDItem(8, '8th item', 'Done'),
        TDItem(9, '9th item', 'To-Do'),
        TDItem(10, '10th item', 'To-Do'),
        TDItem(11, '11th item', 'Done'),
        TDItem(12, '12th item', 'Done')
    ]

def testDoing(testItems):
    itemModel = ViewModel(testItems)
    assert len(itemModel.doingItems) == 4

def testDone(testItems):
    itemModel = ViewModel(testItems)
    assert len(itemModel.doneItems) == 5

def testToDo(testItems):
    itemModel = ViewModel(testItems)
    assert len(itemModel.toDoItems) == 3
