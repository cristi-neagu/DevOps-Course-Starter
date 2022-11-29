from flask import Flask
from flask import render_template
from flask import request

from todo_app.flask_config import Config
import todo_app.data.session_items as session_items

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    '''Main page'''
    return render_template(r'index.html', items=session_items.get_items())

@app.route('/addItem', methods=['POST'])
def addItem():
    '''Add a new item to the list'''
    session_items.add_item(request.form.get('title'))
    return render_template(r'index.html', items=session_items.get_items())
