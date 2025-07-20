from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL

class BlogGeneratorForm(FlaskForm):
    """Form for submitting a YouTube video URL to generate a blog post."""
    
    youtube_url = StringField(
        'YouTube Video URL',
        validators=[
            DataRequired(message="Please enter a YouTube URL."),
            URL(message="Please provide a valid URL.")
        ],
        render_kw={"placeholder": "e.g., https://www.youtube.com/watch?v=..."}
    )
    
    submit = SubmitField('Generate Blog Post')
