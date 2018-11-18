from flask import render_template,abort,redirect,url_for,request,abort
from . import main
from flask_login import login_required, current_user
from ..models import User, Joke, Commentjoke, Pickup, Commentlines, Debate, Commentdebate
from .forms import PitchForm, CommentForm, UpdateProfile
from .. import db, photos

@main.route('/')
@login_required 
def index():
    """
    View root page function that returns the index page and its data
    """
    title = "Welcome to Pitches || Website for pitching ideas"
    return render_template('index.html', title = title)


@main.route('/jokes/')
@login_required
def joke():
    """
    View joke category and its pitches
    """
    jokes = Joke.query.all()
    if jokes is None:
        abort(404)
    return render_template('jokes.html', jokes=jokes)

@main.route('/pick-up/')
@login_required
def lines():
    """
    View pickup-lines category and its pitches
    """
    lines = Pickup.query.all()
    if lines is None:
        abort(404)
    return render_template('pickup-lines.html', lines=lines)

@main.route('/debate/')
@login_required
def debate():
    """
    View debate category and its pitches
    """
    debates = Debate.query.all()
    if debates is None:
        abort(404)
    return render_template('debate.html', debates=debates)

@main.route('/joke/new-joke/', methods=['GET', 'POST'])
@login_required
def new_joke():
    """
    Function that enables one to pitch a new joke 
    """
    form = PitchForm()
 
    if form.validate_on_submit():
        content = form.content.data
        new_joke = Joke(content = content,user_id = current_user.id)
        new_joke.save_joke()
        return redirect(url_for('main.joke'))
    return render_template('new-pitch.html',form=form)

@main.route('/view-joke/<int:id>', methods=['GET', 'POST'])
@login_required
def view_joke(id):
    """
    Returns the joke to be commented on
    """
    print(id)
    jokes = Joke.query.get(id)
    comments = Commentjoke.get_comments(id)
    return render_template('view.html', jokes=jokes, comments=comments, id=id)
@main.route('/comment/<int:id>', methods=['GET', 'POST'])
@login_required
def joke_comment(id):
    """
    Function to post joke comments on specific joke
    """ 
    form = CommentForm() 
    jokes = Joke.query.filter_by(id=id).first()
    if form.validate_on_submit():
        description = form.description.data
        new_comment = Commentjoke(description=description, user_id=current_user.id, joke_id=jokes.id)
        new_comment.save_comment()
        return redirect(url_for('.joke', id=jokes.id))  
    return render_template('comments.html',form=form,jokes=jokes)


@main.route('/pickup/new-line/', methods=['GET', 'POST'])
@login_required
def new_line():
    """
    Function that enables one to pitch a new pick-up line
    """
    form = PitchForm()
 
    if form.validate_on_submit():
        content = form.content.data
        new_line = Pickup(content = content,user_id = current_user.id)
        new_line.save_pickup()
        return redirect(url_for('.lines'))
    return render_template('new-pitch.html',form=form)

@main.route('/view-line/<int:id>', methods=['GET', 'POST'])
@login_required
def view_line(id):
    """
    Returns the pick-up line to be commented on
    """
    print(id)
    lines = Pickup.query.get(id)
    comments = Commentlines.get_commentsl(id)
    return render_template('viewl.html', lines=lines, comments=comments, id=id)
@main.route('/comment-lines/<int:id>', methods=['GET', 'POST'])
@login_required
def line_comment(id):
    """
    Function to post joke comments on specific joke
    """ 
    form = CommentForm() 
    lines = Pickup.query.filter_by(id=id).first()
    if form.validate_on_submit():
        description = form.description.data
        new_comment = Commentlines(description=description, user_id=current_user.id, pickup_id=lines.id)
        new_comment.save_commentl()
        return redirect(url_for('.lines', id=lines.id))  
    return render_template('comments.html',form=form,lines=lines)


@main.route('/debate/new-debate/', methods=['GET', 'POST'])
@login_required
def new_debate():
    """
    Function that enables one to pitch a new debate topic
    """
    form = PitchForm()
 
    if form.validate_on_submit():
        content = form.content.data
        new_debate = Debate(content = content,user_id = current_user.id)
        new_debate.save_debate()
        return redirect(url_for('.debate'))
    return render_template('new-pitch.html',form=form)

@main.route('/view-debate/<int:id>', methods=['GET', 'POST'])
@login_required
def view_debate(id):
    """
    Returns the debate to be commented on
    """
    print(id)
    debates = Debate.query.get(id)
    comments = Commentdebate.get_commentsd(id)
    return render_template('viewdeb.html', debates=debates, comments=comments, id=id)
@main.route('/comment-debates/<int:id>', methods=['GET', 'POST'])
@login_required
def debate_comment(id):
    """
    Function to post debate comments on a specific topic
    """ 
    form = CommentForm() 
    debates = Debate.query.filter_by(id=id).first()
    if form.validate_on_submit():
        description = form.description.data
        new_comment = Commentdebate(description=description, user_id=current_user.id, debate_id=debates.id)
        new_comment.save_commentd()
        return redirect(url_for('.debate', id=debates.id))  
    return render_template('comments.html',form=form,debates=debates)
     
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