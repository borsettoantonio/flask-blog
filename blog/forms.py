from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import BooleanField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired("Campo Obbligatorio!")])
    password = PasswordField('Password', validators=[DataRequired("Campo Obbligatorio!")])
    remember_me = BooleanField('Ricordami')
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    title = StringField('Titolo', 
        validators=[DataRequired("Campo Obbligatorio!"), Length(min=3, max=120, message="Assicurati che il titolo abbia tra i 3 e i 120 caratteri.")])
    description = TextAreaField('Descrizione',
        validators=[Length(max=240, message="Assicurati che il campo descrizione non superi i 240 caratteri.")])
    body = TextAreaField('Contenuto', 
        validators=[DataRequired("Campo Obbligatorio!")])
    markdown = BooleanField('Attiva Markdown')
    image = FileField('Copertina Articolo', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Pubblica Post')

class RegistraForm(FlaskForm):
    nome = StringField('Nome', 
        validators=[DataRequired("Campo Obbligatorio!"), Length(min=3, max=30, message="Assicurati che il nome abbia tra i 3 e i 120 caratteri.")])
    cognome = StringField('Cogome', 
        validators=[DataRequired("Campo Obbligatorio!"), Length(min=3, max=30, message="Assicurati che il nome abbia tra i 3 e i 120 caratteri.")])
    username = StringField('User Name',
        validators=[DataRequired("Campo Obbligatorio!"), Length(max=12, message="Assicurati che il campo descrizione non superi i 12 caratteri.")])
    email = StringField('e-mail',
        validators=[DataRequired("Campo Obbligatorio!"), Length(max=50, message="Assicurati che il campo descrizione non superi i 50 caratteri.")])
    password = StringField('Password', validators=[DataRequired("Campo Obbligatorio!"),Length(min=3, max=25, message="Assicurati che il nome abbia tra i 3 e i 25 caratteri.")])
    ripeti_password = StringField('Ripeti la password', validators=[DataRequired("Campo Obbligatorio!"),Length(min=3, max=25, message="Assicurati che il nome abbia tra i 3 e i 25 caratteri.")])
    image = FileField('La tua immagine', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Registra')

