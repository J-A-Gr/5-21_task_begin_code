from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from datetime import datetime
# from sqlalchemy.orm import relationship

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
    posts = db.relationship('Post', back_populates='author')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', back_populates='posts')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Repeat Password', validators=[DataRequired(),
                                      EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')  # TODO 2 ../..
def home():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password_unhashed = form.password.data  # TODO 5.
        password = bcrypt.generate_password_hash(password_unhashed) # TODO 5.

        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username already exists", "error")
            return render_template('register.html', form=form)

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("User successfully registered", "success")
        return redirect(url_for('login'))
    
    for field, errors in form.errors.items():
        for error in errors:
            flash(error, 'error')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("User is logged in", "success")
            return redirect(url_for('home'))
        else:
            flash("Incorect password", "error")
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        post = Post(title=title, content=content, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)



@app.route('/logout')
@login_required
def logout():
    logout_user()  # TODO 4.
    flash("You have logged out", "success")
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)