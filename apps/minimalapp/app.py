from flask import Flask, render_template, url_for
from flask import request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from email_validator import validate_email, EmailNotValidError
import logging
import os
from flask_mail import Mail, Message


# flask 클래스를 인스턴스화 한다.
app=Flask(__name__)
# app.debug = True
app.config["SECRET_KEY"] = "2sadsad34asdJS"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 

# mail클래스의 config를 추가한다.
app.config["MAIL_SERVER"]=os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"]=os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"]=os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"]=os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"]=os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"]=os.environ.get("MAIL_DEFAULT_SENDER")

# 메일 클래스 인스턴스(객체)생성
mail = Mail(app)
# 디버그툴바확장 클래스 인스턴스(객체)생성
toolbar = DebugToolbarExtension(app)

# logger의 레벨을 DEBUG로 설정
app.logger.setLevel(logging.DEBUG)

# app.logger.critical("fatal error")
# app.logger.error("error")
# app.logger.debug("debug")
# app.logger.info("info")

with app.test_request_context("/users?updated=true"):
    print(request.args.get("updated"))

#URL과 실행할 함수를 맵핑한다.
# '127.0.0.1:5000:/'
@app.route("/")
def index():
    return "Hello, Flaskbook!"

@app.route("/hello/<name>",
           methods=["GET","POST"],
           endpoint="hello-endpoint")
def hello(name):
    return render_template("index.html", name=name)

@app.route("/hello2/<name>",
           methods=["GET","POST"])
def show_name(name):
    return render_template("index.html", name=name)

# @app.route("/light_check/<command>",
#            methods=["GET","POST"])
# def light_check(command):
#     return render_template("light_check.html", command=command)

@app.route("/contact")
def contact():
    return render_template("contact.html")

# 메일을 송신하는 함수
# 인수 : 누구에게,제목,내용
def send_email(to, subject, template,**kwargs):
    # 메일을 어떤제목으로, 누구에게 보낼지 설정 
    msg = Message(subject, recipients=[to])
    # 메일 내용을 txt로 생성
    #msg.body = render_template(template+".txt",**kwargs)
    # 메일 내용을 html로 생성
    msg.html = render_template(template+".html",**kwargs)
    # 메일을 송신
    mail.send(msg)

@app.route("/contact/complete", methods=["GET","POST"])
def contact_complete():
    # 내용 보내기라면...
    if request.method=="POST":
        # 입력받은 값을 python변수로 받아오기
        username = request.form["username"]
        email=request.form["email"]
        description = request.form["description"]

        # 메일 보내기 구현

        # 입력 체크
        is_valid = True

        if not username:
            flash("사용자명은 필수입니다.")
            is_valid = False
        
        if not email:
            flash("메일 주소는 필수입니다.")
            is_valid = False            

        # 이메일이 유효한지 체크
        try:
            # validate_email함수가 실행되고 메일이 
            # 유효하지 않으면 except로 이동한다.
            validate_email(email)

        except EmailNotValidError as e:
            flash("메일 주소의 형식으로 입력해 주세요.")
            flash(str(e))
            is_valid = False

        if not description:
            flash("문의 내용은 필수입니다.")
            is_valid = False   
        
        if not is_valid:
            print("is_valid=False")
            return redirect(url_for("contact"))
        
        #함수를 생성
        send_email(email,
                   "문의 감사합니다",
                   "contact_mail",
                   username=username,
                   description=description
                   )


        # contact_complete 엔드포인트로 redirect한다.
        return redirect(url_for("contact_complete"))
    
    return render_template("contact_complete.html")

# with app.test_request_context():
#     # / 
#     print(url_for("index"))
#     # /hello/world
#     print(url_for("hello-endpoint", name="world"))
#     print(url_for("hello-endpoint", name=""))
#     # /name/AK?page=1
#     print(url_for("show_name", name="AK", page="1"))