from flask import Flask
from flask import render_template

from todo_app.flask_config import Config
import todo_app.data.session_items as session_items

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    return render_template(r'index.html', items=session_items.get_items())
