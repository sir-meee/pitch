from flask import render_template,abort,redirect,url_for,request
from . import main
from flask_login import login_required,current_user
from ..models import Pitch, User,Comment,Upvote,Downvote
from .forms import PitchForm, CommentForm,UpdateProfile
from .. import db, photos

@main.route('/', methods = ['GET','POST'])
def index():
    """
    View root page function that returns the index page and its data
    """
    title = title = "Welcome to Pitches || Website for pitching ideas"
    return render_template('index.html', title = title)

@main.route('/pitches/new', methods = ['GET','POST'])
@login_required
def new_pitch():
    """
    View new pitch function that returns new pitches and its data
    """
    form = PitchForm()
    if form.validate_on_submit():
        content = form.content.data
        category = form.category.data
        new_pitch = Pitch(content=content, category=category)
        db.session.add(new_pitch)
        db.session.commit()
    return render_template('new-pitch.html',form=form)

@main.route('/comments/new/<int:pitch_id>', methods = ['GET','POST'])
@login_required
def new_comment(pitch_id):
    """
    View new comment function that returns the comment page and its data
    """
    form = CommentForm()
    pitch=Pitch.query.get(pitch_id)
    if form.validate_on_submit():
        description = form.description.data
        new_comment = Comment(description=description, pitch_id = pitch_id)
        db.session.add(new_comment)
        db.session.commit()
    all_comments = Comment.query.filter_by(pitch_id = pitch_id).all()
    return render_template('comments.html',form=form, pitch=pitch, comment=all_comments)

@main.route('/pitches/upvote/<int:pitch_id>/upvote', methods = ['GET','POST'])
@login_required
def upvote(pitch_id):
    """
    Adds an upvotes to pitches
    """
    pitch = Pitch.query.get(pitch_id)
    user = current_user
    pitch_upvotes = Upvote.query.filter_by(pitch_id= pitch_id)
    new_upvote = Upvote(pitch_id=pitch_id,user= current_user)
    new_upvote.save_upvotes()

@main.route('/pitches/downvote/<int:pitch_id>/downvote', methods = ['GET','POST'])
@login_required
def downvote(pitch_id):
    """
    Adds downvotes to pitches
    """ 
    pitch = Pitch.query.get(pitch_id)
    user = current_user
    pitch_downvotes = Upvote.query.filter_by(pitch_id= pitch_id)
    new_downvote = Downvote(pitch_id=pitch_id,user= current_user)
    new_downvote.save_downvotes()

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    form = UpdateProfile()
    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.profile',uname=user.username))
    return render_template('profile/update.html',form =form)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))    