from flask import Blueprint, redirect, render_template, session, url_for, flash

from app.config.urlMiApi import BASE_URL
from app.logs.capturaDeError import logException
from app.src.forms.signUp import SignUpForm
from app.src.token.auth import authenticate
from app.src.token.peticionesProtegidas import postRequest, protectedRequest
from pydantic import BaseModel, Field

class UsuarioRegister(BaseModel):
    nombre: None | str = Field(None, max_length=50)
    apellido: None | str = Field(None, max_length=50)
    username: str = Field(..., max_length=50)
    email: str = Field(..., max_length=50)
    pwd: str = Field(..., min_length=1)
    verifyPwd: str = Field(...)

signUp: Blueprint = Blueprint(name='signUp', import_name=__name__)

@signUp.route('/', methods=['GET', 'POST'])
def register():
    try:
        formularioSignUp: SignUpForm = SignUpForm()
        if formularioSignUp.validate_on_submit():  
            
            data = {
            "nombre": formularioSignUp.nombre.data,
            "apellido": formularioSignUp.apellido.data,
            "username": formularioSignUp.username.data,
            "email": formularioSignUp.email.data,
            "pwd": formularioSignUp.pwd.data,
            "verifyPwd": formularioSignUp.pwdVerify.data
            }
            respuesta = postRequest(endpoint="/usuario/register", data=data)
            if not respuesta['response']:
                error = respuesta['message']
                # logException(exception=Exception(respuesta['message']))
                flash(message=error, category='danger')
                return redirect(url_for('signUp.register'))       
            return redirect(url_for('signIn.iniciarSesion')) 
        return render_template('register.html', form=formularioSignUp)
    except Exception as e:
        logException(e)
        return redirect(url_for('home'))