from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField

class researchForm(FlaskForm):
    research = StringField('Recherche')
    magazineCheck = BooleanField('Magasines')
    bookCheck = BooleanField('Livres')
    submit = SubmitField('Chercher')
