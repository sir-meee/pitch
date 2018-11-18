from flask_wtf import FlaskForm
from wtforms import SubmitField,TextAreaField
from wtforms.validators import Required
from wtforms import ValidationError


class PitchForm(FlaskForm):
    content = TextAreaField("What would you like to pitch ?",validators=[Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    description = TextAreaField('Add comment',validators=[Required()])
    submit = SubmitField()

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')