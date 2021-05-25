import bcrypt
from flask import Flask, render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_migrate import Migrate
from app.config import Config

app = Flask(__name__, static_folder='public')
app.config.from_object(Config)

Session(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.models import *
from app.admin import *

try:
    db.create_all()
except:
    pass

@app.route('/', methods=["GET"])
def index():
    if 'user' in session:
        return redirect(f"/user/{session['user']['id']}")
    return redirect('/auth/login')


@app.route('/auth/login', methods=["GET", "POST"])
def user_login():
    if 'user' in session:
        return redirect(f"/user/{session['user']['id']}")
    if request.method == "POST":
        if request.form.get('mail') and request.form.get('pwd'):
            password = u"%s"%(request.form.get('pwd'))
            pros_user = User.query.filter(User.email == request.form.get('mail')).first()
            if pros_user:
                if bcrypt.checkpw(password.encode('utf-8'), pros_user.password):
                    session['user'] = {'id': pros_user.id, 'adminStatus': pros_user.isAdmin, 'userType': pros_user.usertype }
                    return redirect(f'/user/{pros_user.id}')
                return redirect('/auth/login')
            return redirect('/auth/login')
        return redirect('/auth/login')
    return render_template('login.html')


@app.route('/auth/logout', methods=["GET"])
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/user/<user_id>', methods=["GET", "POST"])
def user_operations(user_id):
    return render_template('index.html', isAdmin=session['user']['adminStatus'])



with app.app_context():
    if db.engine.url.drivername == 'sqlite':
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)