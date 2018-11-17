from flask import render_template
from . import main
 @main.route('/')
def index():
    """
    View root page function that returns the index page and its data
    """
    title = "Pitches"
    return render_template('index.html', title = title)
