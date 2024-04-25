# app.py
from typing import Optional

import sqlalchemy
from flask import Flask, session, render_template, redirect, request, url_for
from auth_security.app import auth
from db.commands import ORMCommands
from db.models import Base
from db.database import Base, sync_engine


app = Flask(__name__)
app.register_blueprint(auth)

Base.metadata.create_all(sync_engine)

app.config["SECRET_KEY"] = "afghds443df134gadg55"
app.config["SESSION_TYPE"] = "filesystem"




@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error='Такая страница отсутствует')


@app.errorhandler(500)
def page_not_found(e):
    return render_template('error.html', error='Какая-то ошибка')


@app.errorhandler(sqlalchemy.exc.IntegrityError)
def internal_error(error):
    return render_template('registration.html', error='Пользователь с таким именем уже создан')


@app.route('/')
def index():

    if session.get('role'):
        return render_template('index.html', context={'user': session.get('user')})

    return render_template('index.html')


@app.route('/delete/<idx>', methods=['POST'])
def delete(idx: int):
    ORMCommands.delete_user(idx)
    return redirect(url_for('admin'))


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    consumers = ORMCommands.get_all_consumers()
    implementers = ORMCommands.get_all_implementers()
    return render_template('admin.html', consumers=consumers, implementers=implementers)


@app.route('/consumers/<idx>', methods=['GET'])
@app.route('/consumers', methods=['GET'])
def consumers(idx: Optional[int] = None):

    if idx:
        consumer = ORMCommands.get_one_user(idx)
        return render_template('one_user.html', user=consumer)

    consumers = ORMCommands.get_all_consumers()
    return render_template('implementer.html', consumers=consumers)


@app.route('/implementers/<idx>', methods=['GET'])
@app.route('/implementers', methods=['GET'])
def implementers(idx: Optional[int] = None):

    if idx:
        implementer = ORMCommands.get_one_user(idx)
        return render_template('one_user.html', user=implementer)

    implementers = ORMCommands.get_all_implementers()
    return render_template('consumer.html', implementers=implementers)


if __name__ == '__main__':
    app.run(debug=True)
