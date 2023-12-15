from flask import Blueprint, render_template
from flask import redirect, url_for
from apps.crud.forms import UserForm
from apps.crud.models import User
from apps.app import db

crud = Blueprint("crud",
                 __name__, 
                 template_folder="templates",
                 static_folder="static")


@crud.route("/")
def index():
    return render_template("crud/index.html")

# "127.0.0.1:5000/crud/user/new"
@crud.route("/users/new", methods=["GET","POST"])
def create_user():
    # views.py파일에 생성된 class의 인스턴스를 생성
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )

        # SQLAlchemy를 사용하여 데이터베이스에 ISERT
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("crud.users"))
    return render_template("crud/create.html", form=form)

@crud.route("/sql")
def sql():
    db.session.query(User).all()
    return "콘솔 로그를 확인해 주세요."

@crud.route("/users")
def users():
    users = db.session.query(User).all()
    return render_template("crud/index.html", users=users)

@crud.route("/users/<user_id>", methods=["GET","POST"])
def edit_user(user_id):
    form = UserForm()
 ## test
    user= User.query.filter_by(id=user_id).first()

    if form.validate_on_summit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("crud.users"))
    
    return render_templates("crud/edit.html", user=user, form=form)



