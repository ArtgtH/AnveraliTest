from flask_bcrypt import Bcrypt

from flask import Blueprint, request, render_template, session

from auth_security.schemas import UserDTO

from db.commands import ORMCommands


auth = Blueprint('auth', __name__, url_prefix='/auth')
bcrypt = Bcrypt()


@auth.route('/logout', methods=['GET'])
def logout():
    if session.get('role'):
        session.pop('role')

    return render_template('login.html', msg='You just unlogged in')


@auth.route('/login', methods=['GET', 'POST'])
def login():

    if session.get('role'):
        return render_template('index.html', msg='You are already logged in')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = ORMCommands.login_user(username)
        if bcrypt.check_password_hash(user.password, password):
            session['role'] = user.role
            return render_template('index.html')
        else:
            return render_template('login.html', msg='Wrong credentials')

    return render_template('login.html')


@auth.route('/registration', methods=['GET', 'POST'])
def registration():

    if session.get('role'):
        return render_template('index.html', msg='You are already logged in')

    if request.method == 'POST':

        user = UserDTO(**dict(request.form))

        user.password = bcrypt.generate_password_hash(user.password).decode('utf-8')

        ORMCommands.register_new_user(user)

        session['role'] = user.role

        return render_template('index.html')

    return render_template('registration.html')

