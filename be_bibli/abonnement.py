from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField


class AbonnementForm(FlaskForm):
  nomUtilisateurs = StringField('Nom')
  prenomUtilisateurs = StringField('Prenom')
  utilisateursAge = IntegerField('Age')
  utilisateursAddresseNumero = IntegerField('numero')
  utilisateursAddresseRue = StringField('street')
  utilisateursAddresseCode = StringField('code')
  utilisateursCourriel = StringField('Courriel')
  utilisateursMdp = PasswordField('Mot de passe')
  submit = SubmitField('connexion')