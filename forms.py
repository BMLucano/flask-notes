from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length, Email


class RegisterForm(FlaskForm):
    """Form for registering a user"""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(max=20)]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired()]
    )
    #import email_validator???
    email = StringField(
        "Email",
        validators=[InputRequired(), Length(max=50), Email()]
    )

    first_name= StringField(
        "First Name",
        validators=[InputRequired(), Length(max=30)]
    )

    last_name = StringField(
        "Last Name",
        validators=[InputRequired(), Length(max=30)]
    )


class LoginForm(FlaskForm):
    """Form for logging in a user"""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(max=20)]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired()]
    )

class NoteForm(FlaskForm):
    """Form to add a note"""

    title = StringField(
        "Title",
        validators=[InputRequired(), Length(max=100)]
    )

    content = TextAreaField(
        "Content",
        validators=[InputRequired()]
    )


class CSRFProtectForm(FlaskForm):
    """CSRF Protection"""




