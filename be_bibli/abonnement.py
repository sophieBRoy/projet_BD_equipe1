from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField


class AbonnementForm(FlaskForm):
  nomUtilisateurs = StringField('Nom')
  prenomUtilisateurs = StringField('Prenom')
  utilisateursAge = IntegerField('Age')
  utilisateursAddresse = StringField('Adresse')
  utilisateursCourriel = StringField('Courriel')
  utilisateursMdp = PasswordField ('Mot de passe')
  submit = SubmitField('connexion')