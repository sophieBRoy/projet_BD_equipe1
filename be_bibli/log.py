from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField


class LogForm(FlaskForm):
  nomUser = StringField('courriel')
  passUser = PasswordField('mot de passe')
  submit = SubmitField('connexion')