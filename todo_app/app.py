from flask import Flask
from flask import render_template, redirect, url_for, flash
from flask import request

from todo_app.flask_config import Config
import todo_app.data.session_items as session_items

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    '''Main page'''
    return render_template('index.html', items=session_items.get_items())

@app.route('/changeItem', methods=['POST'])
def changeItem():
    '''Can create, edit, and delete an item'''
    reqAction = request.form.get('changeItem')

    if reqAction == 'Add Item':
        itemTitle = request.form.get('itemTitle')
        if itemTitle == "":
            flash('ERROR: No title specified for new item')
        else:
            session_items.add_item(itemTitle)

    if reqAction == 'Delete Item':
        itemID = request.form.get('itemID')
        if itemID == "":
            flash('ERROR: No ID specified for item to be deleted')
        else:
            session_items.delete_item(itemID)

    if reqAction == 'Get Item':
        itemID = request.form.get('itemID')
        if itemID == "":
            flash('ERROR: No ID specified for item to be retrieved')
        else:
            item = session_items.get_item(itemID)
            itemStart = item['status'] == 'Started'
            itemTitle = item['title']
            return render_template('index.html', items=session_items.get_items(),
                                    setID=itemID, setStart=itemStart, setTitle=itemTitle)

    if reqAction == "Save Item":
        itemID = request.form.get('itemID')
        if itemID == "":
            itemTitle = request.form.get('itemTitle')
            session_items.add_item(itemTitle)
        else:
            items = session_items.get_items()
            itemStart = request.form.get('isStarted') is not None
            itemTitle = request.form.get('itemTitle')
            for item in items:
                if item['id'] == int(itemID):
                    item['title'] = itemTitle
                    item['status'] = 'Started' if itemStart else 'Not started'
                    session_items.save_item(item)
                    break
            else:
                session_items.add_item(itemTitle)

    return redirect(url_for('index'))
