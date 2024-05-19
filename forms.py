from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,URLField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField

class PostForm(FlaskForm):
    title=StringField("Title of Your Recipe",validators=[DataRequired()],render_kw={"placeholder":"Most Delicious Soup"})
    subtitle=StringField("Subtitle",render_kw={"placeholder":"Learn how to cook soup"})
    body=CKEditorField("Recipe Content",validators=[DataRequired()])
    img_url=URLField("Image url",validators=[DataRequired()])
    submit=SubmitField("Submit Post", render_kw={"class": "btn btn-success my-2"})

class CommentForm(FlaskForm):
    comment=CKEditorField("Comment",validators=[DataRequired()])
    submit=SubmitField("Submit Comment")