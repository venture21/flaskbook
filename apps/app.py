from flask import Flask
from pathlib import Path
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

# SQLAlchemy 인스턴스를 생성한다.
db = SQLAlchemy()

# CSRF 인스턴스 생성
csrf = CSRFProtect()

#create_app함수 생성
def create_app():

    # 플라스크 인스턴스(객체)를 생성
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY="googleCloudPlatform",
        SQLALCHEMY_DATABASE_URI=
        f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True, 
        WTF_CSRF_SECRET_KEY="sadasdsdasde32324dfg",
    )

    # SQLAlchemy와 앱을 연결
    db.init_app(app)

    # Migrate와 앱을 연결
    Migrate(app,db)

    # CSRF의 앱을 연결
    csrf.init_app(app)

    from apps.crud import views as crud_views
    #register_blueprint
    app.register_blueprint(crud_views.crud, url_prefix="/crud") 

    return app

