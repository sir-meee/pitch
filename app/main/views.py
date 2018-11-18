from flask import render_template,abort
from . import main
from flask_login import login_required
from ..models import User

@main.route('/')
def index():
    """
    View root page function that returns the index page and its data
    """
    title = "Pitches"
    return render_template('index.html', title = title)

@main.route('/pitches/new', methods = ['GET','POST'])
@login_required
def new_pitch():
    """
    View new pitch function that returns new pitches and its data
    """

@main.route('/comments/new/<int:pitch_id>', methods = ['GET','POST'])
@login_required
def new_comment(pitch_id):
    """
    View new comment function that returns the comment page and its data
    """

@main.route('/pitches/upvote/<int:pitch_id>/upvote', methods = ['GET','POST'])
@login_required
def upvote(pitch_id):
    """
    Adds an upvotes to pitches
    """
 
@main.route('/pitches/downvote/<int:pitch_id>/downvote', methods = ['GET','POST'])
@login_required
def downvote(pitch_id):
    """
    Adds downvotes to pitches
    """ 

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    return render_template("profile/profile.html", user = user)
