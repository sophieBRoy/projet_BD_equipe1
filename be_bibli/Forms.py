from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField

class researchForm(FlaskForm):
    research = StringField('Recherche')
    magazineCheck = BooleanField('Magasines')
    bookCheck = BooleanField('Livres')
    submit = SubmitField('Chercher')

class advancedResearchForm(FlaskForm):
    researchB = StringField('Titre')
    researchA = StringField('Auteur')
    researchO = StringField('Origine')
    submit = SubmitField('Chercher')
    fantaisieCheck = BooleanField('Fantaisie')
    sFCheck = BooleanField('Science-Fiction')
    polarCheck = BooleanField('Polar')
    classiqueCheck = BooleanField('Classique')
    horreurCheck = BooleanField('Horreur')
    bDCheck = BooleanField('Bande-dessinée')
    overratedCheck = BooleanField('Overrated')
    decouvertesCheck = BooleanField('Decouvertes')
    modeCheck = BooleanField('Mode')
    scienceCheck = BooleanField('Science')
    cuisineCheck = BooleanField('Cuisine')
    artCheck = BooleanField('Art')
    adoCheck = BooleanField('Ado')

class adminForm(FlaskForm):
    id = StringField('recherche')
    submit = SubmitField('Appliquer')



