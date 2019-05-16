from flask import *
from functools import wraps

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

request_manager = None
account_manager = None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.get('user') is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
@login_required
def home():
    return render_template("home.html")

@app.route("/login",methods=['POST','GET'])
def login():
    error = None
    if request.method == 'POST':
        if validate_login(request.form['username'],
                          request.form['password']):
            session['username'] = request.form['username']
            return redirect(url_for('home'))
        else:
            error = 'login failed!'
    return render_template('login.html',error=error)

@app.route("/logout")
@login_required
def logout():
    session.pop('username',None)
    return redirect(url_for('logout'))

def validate_login(username,password):
    return get_account_manager().validate_user(username,password)


def start_website(r_manager,a_manager):
    global request_manager,account_manager
    request_manager = r_manager
    account_manager = a_manager
    app.run("0.0.0.0",80)

def get_account_manager():
    global account_manager
    return account_manager
def get_requests_manager():
    global request_manager
    return request_manager