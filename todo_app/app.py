from flask import Flask
from flask import render_template, redirect, url_for, flash
from flask import request

from todo_app.flask_config import Config
import todo_app.data.trello_items as trello_items
from todo_app.data.ViewModel import ViewModel

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())


    @app.route('/')
    def index():
        '''Main page'''
        itemViewModel = ViewModel(trello_items.getItems())
        return render_template('index.html', viewModel=itemViewModel)

    @app.route('/changeItem', methods=['POST'])
    def changeItem():
        '''Can create, edit, and delete an item'''
        reqAction = request.form.get('changeItem')

        if reqAction == 'Add Item':
            itemTitle = request.form.get('itemTitle')
            if itemTitle == "":
                flash('ERROR: No title specified for new item')
            else:
                trello_items.addItem(itemTitle)

        if reqAction == 'Delete Item':
            itemID = request.form.get('itemID')
            if itemID == "":
                flash('ERROR: No ID specified for item to be deleted')
            else:
                trello_items.deleteItem(itemID)

        if reqAction == 'Get Item':
            itemID = request.form.get('itemID')
            if itemID == "":
                flash('ERROR: No ID specified for item to be retrieved')
            else:
                item = trello_items.getItem(itemID)
                if item:
                    itemStart = item.status == 'Doing'
                    itemTitle = item.name
                    return render_template('index.html', items=trello_items.getItems(),
                                        setID=itemID, setStart=itemStart, setTitle=itemTitle)
                else:
                    flash('ERROR: ID not found')

        if reqAction == "Save Item":
            itemID = request.form.get('itemID')
            if itemID == "":
                itemTitle = request.form.get('itemTitle')
                trello_items.addItem(itemTitle)
            else:
                items = trello_items.getItems()
                itemStart = request.form.get('isStarted') is not None
                itemTitle = request.form.get('itemTitle')
                for item in items:
                    if item.id == int(itemID):
                        item.name = itemTitle
                        item.status = 'Doing' if itemStart else 'To Do'
                        trello_items.saveItem(item)
                        break
                else:
                    trello_items.addItem(itemTitle)

        if reqAction == "Complete Item":
            itemID = request.form.get('itemID')
            if itemID == "":
                flash('ERROR: No ID specified for item to be marked as complete')
            else:
                trello_items.completeItem(itemID)

        return redirect(url_for('index'))

    return app
