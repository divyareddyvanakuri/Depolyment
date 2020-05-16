from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_mail import Mail,Message
from werkzeug.security import generate_password_hash,check_password_hash
from flask_wtf.csrf import CSRFProtect,CSRFError
from form import LogInForm,SignUpForm,ForgotPasswordForm,ResetPasswordForm
from models import User
from flask_wtf.csrf import CSRFProtect, CSRFError
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
import os
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

url_serializer = URLSafeTimedSerializer(os.environ.get('secret_key'))
app.config.update(dict(
    SECRET_KEY=os.environ.get('secret_key'),
    WTF_CSRF_SECRET_KEY=os.environ.get('CSRF_SECRET_KEY')
))

app.config.update(
	#EMAIL SETTINGS
   MAIL_DEBUG =True,
   MAIL_SERVER='smtp.gmail.com',
   MAIL_PORT=465,
   MAIL_USE_SSL=True,
   MAIL_USE_TLS = False,
   MAIL_USERNAME = os.environ.get('email_username'),
   MAIL_PASSWORD = os.environ.get('email_password'),
   MAIL_DEFAULT_SENDER = os.environ.get('email_username'),
	)

mail = Mail(app)
csrf = CSRFProtect(app)

@app.route('/home')
def home():
   return render_template("home.html")

@app.route('/login',methods=["GET","POST"])
def login():
   form = LogInForm()
   if form.validate_on_submit():
      username = form.username.data
      password = form.password.data
      user = User.query.filter_by(username=username).first()
      try:
         if check_password_hash(user.password, password):
            if user.is_active:
               session["username"] = user.username
               session["email"] = user.email
               return render_template("home.html")
            else:
               return "please active account before login"
      except UnicodeError as err:
         flash("somthing went wrong:",err)

   return render_template("login.html",form=form)

@app.route("/logout")
def logout():
   session.clear()
   return render_template("home.html")

@app.route('/register',methods=["GET","POST"])
@csrf.exempt
def register():
   form=SignUpForm()
   if form.validate_on_submit():
      username = form.username.data
      email = form.email.data
      password = form.password.data
      confirmpassword = form.confirmpassword.data
      if password == confirmpassword:
         hash_password = generate_password_hash(password,method="sha256")
         user = User(username=username, email=email,password=hash_password)
         try:
            user.save(user)
         except (IntegrityError,TypeError) as err:
            user.rollBack()
            return "duplicate user details,please confirm once again with user details"
      token = url_serializer.dumps(email,salt='email-confirm')
      msg = Message('Activate',sender='divyavanakuri1234@gmail.com',recipients=[email])
      link = url_for('activate',token=token,_external=True)
      msg.body = render_template("activate.html",link=link,email=email)
      print(msg)
      mail.send(msg)
      return "registeration done successfully,please activate account through mailed link"
   return render_template("register.html",form=form)


@app.route('/activate/<token>',methods=["GET","POST"])
def activate(token):
   try:
      email = url_serializer.loads(token,salt='email-confirm')
      print(email)
      user = User.query.filter_by(email=email).first()
      print(user)
      if user:
         user.is_active = True
         user.update()
      else:
         return "invalide details"
      return "Your account activated successfully,please login"
   except SignatureExpired:
      return '<h1>the token is expired</h1>'
   

@app.route('/forgotpassword',methods=["GET","POST"])
def forgotpassword():
   if request.method == "POST":
      email = request.form["email"]
      token = url_serializer.dumps(email,salt='email-confirm')
      msg = Message('ResetPassword',sender='divyavanakuri1234@gmail.com',recipients=[email])
      link = url_for('resetpassword',token=token,_external=True)
      msg.body = render_template("sent.html",link=link,email=email)
      print(msg)
      mail.send(msg)
      return "Email was sent successfully to your account"
   return render_template('forgotpassword.html')


@app.route('/resetpassword/<token>')
def resetpassword(token):
   if request.method == "POST":
      password = request.form["password"]
      confirmpassword = request.form["confirmpassword"]
      try:
         email = url_serializer.loads(token,salt='email-confirm')
         user =User.query.filter_by(email=email).first()
         if user: 
            hash_password = generate_password_hash(password,method="sha256")  
            user.password = hash_password
            user.update()
         else:
            return redirect("/")
      except SignatureExpired:
         return '<h1>the token is expired</h1>'
      # flash("your password successfully updated","success")
      return redirect('/login')
   return render_template("resetpassword.html")


if __name__ == '__main__':
   app.run(debug=True,host='0.0.0.0')