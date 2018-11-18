from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,TextAreaField,RadioField
from wtforms.validators import Required
from wtforms import ValidationError

class PitchForm(FlaskForm):
    content = TextAreaField("What would you like to pitch ?",validators=[Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
 description = TextAreaField('Add comment',validators=[Required()])
submit = SubmitField()

#class Downvote(FlaskForm):
#   submit = SubmitField()

class CategoryForm(FlaskForm):
    """
    Class to create a wtf form for creating a pitch
    """
    name =  StringField('Category Name', validators=[Required()])
    submit = SubmitField('Add')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')