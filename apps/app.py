from flask import Flask

#create_app함수 생성
def create_app():

    # 플라스크 인스턴스(객체)를 생성
    app = Flask(__name__)

    from apps.crud import views as crud_views

    #register_blueprint
    app.register_blueprint(crud_views.crud, url_prefix="/crud") 

    return app

    