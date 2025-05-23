from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'ixlqec7($q$7u2x7o@ixqt2pr-$i)v3_sn7lcn_%pk^*m--tt0'  # Change this to a secure secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Change the database URI as per your needs
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'home'

bcrypt = Bcrypt(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')  # TODO 2 ../..
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password_unhashed = request.form['password']  # TODO 5.

        password = bcrypt.generate_password_hash(password_unhashed) # TODO 5.

        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username already exists", "error")
            return render_template('register.html')
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("User successfully registered", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("User is logged in", "success")
            return redirect(url_for('home'))
        else:
            flash("Incorect password", "error")
            return render_template('login.html')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()  # TODO 4.
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)