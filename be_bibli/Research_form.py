from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class researchForm(FlaskForm):
    research = StringField('Recherche')
    submit = SubmitField('Chercher')