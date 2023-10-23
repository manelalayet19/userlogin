
import flask
import json
from flask import Flask, request, session, redirect, url_for, render_template, flash, send_from_directory, render_template_string
import os
import pathlib
import requests
from flask import Flask, session, abort, redirect, request, url_for
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import google.auth.transport.requests
import psycopg2
import psycopg2.extras
from flask_dance.contrib.azure import make_azure_blueprint, azure
from authlib.integrations.flask_client import OAuth
from oauthlib.oauth2.rfc6749.errors import MismatchingStateError
from flask_dance.contrib.github import make_github_blueprint, github
from flask_mail import Mail, Message
import re
import uuid

GOOGLE_CLIENT_ID = "685088020931-1p51a578imjefbst8ngrjct85gc18qqe.apps.googleusercontent.com"
conn = psycopg2.connect(dbname="manel", user="manel",
                        password="manel$2020", host="igeomedia.com")

app = Flask(__name__)
oauth = OAuth(app)
mail = Mail(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'geopovnet@gmail.com'
app.config['MAIL_PASSWORD'] = 'admin5612!'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# azure setup
azure_bp = make_azure_blueprint(
    client_id="a5262ced-03fd-4095-b2fd-200b50ead86f",
    client_secret="GsZ8Q~CCRdkxRJDeK1H_ruGgG1eKNUmRvKQXlaT-",
    redirect_to="getAToken",
    redirect_url="http://localhost:5000/getAToken"
)
app.register_blueprint(azure_bp, url_prefix="/login")

github_blueprint = make_github_blueprint(
    client_id="107d7c5714f516c08faa",
    client_secret="1af3ad719f9930bb5cba4c469edff482c672f226",
)
app.register_blueprint(github_blueprint, url_prefix="/login")

"""
google : Erreur 400 : redirect_uri_mismatch --fixed 
the uri mismatch fixed  both miccrosoft and google looking for apple 
the google section is not working correctly - uri mismatch i need to review the uri provided in the google console - 400 error 
MISCROSFT azure its working on localhost for now until i change the invalid_request 
The provided value for the input parameter 'redirect_uri' is not valid. The expected value is a URI which matches a redirect URI registered for this client application.
invalid_request: The provided value for the input parameter 'redirect_uri' is not valid. The expected value is a URI which matches a redirect URI registered for this client application.
"""
# google setup
app.secret_key = uuid.uuid4().hex
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
client_secret_file = os.path.join(
    pathlib.Path(__file__).parent, "client_secret.json")
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secret_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://localhost:5000/callback"
)


@app.errorhandler(MismatchingStateError)
def handle_mismatching_state_error(e):
    return "MismatchingStateError: " + str(e), 400


def google_login_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return redirect(url_for('login'))
        else:
            return function()

    return wrapper


@app.route('/')
def index():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    else:
        return render_template('inscription.html')

@app.route('/chatbot')
def chatbot() : 
    return render_template('chatbot.html')
# auth microsoft
@app.route("/getAToken")
def get_token():
    if not azure.authorized:
        flash('You need to log in with Azure AD first.', 'danger')
        return redirect(url_for("azure.login"))
    resp = azure.get("https://graph.microsoft.com/v1.0/me")
    if not resp.ok:
        flash('Failed to fetch user data from Azure AD.', 'danger')
        return redirect(url_for('index'))
    return "You are {email} on Azure AD".format(email=resp.json()["userPrincipalName"])


@app.route('/signup')
def signup():
    return render_template('login.html')


@app.route('/login')
def login():
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    return redirect(authorization_url)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route("/protected_area")
@google_login_required
def protected_area():
    user_info = f"Hello {session['name']}!<br/>"
    user_info += f"Email: {session['email']}<br/>"
    user_info += f"<img src='{session['picture']}' alt='Profile Picture' /><br/>"
    user_info += "<a href='/logout'><button>Logout</button></a>"
    return user_info


@app.route('/profile')
def profile():

    if 'loggedin' in session:
        return render_template('profile.html', username=session.get('username'),
                               avatar=session.get('avatar'),
                               login=session.get('login'),
                               location=session.get('location'),
                               email=session.get('email'))
    elif github.authorized:
        return redirect(url_for('github.login'))
    else:
        return render_template('inscription.html')


@app.route('/login/github')
def github_login():
    if not github.authorized:
        return redirect(url_for("github.login"))
    return redirect(url_for('authorized'))


@app.route('/login/github/authorized')
def authorized():
    response = github.authorized_response()
    print('oauth event is trigered  !! ')
    print(response, 'response')
    if response is None or response.get('access_token') is None:
        flash('Failed to log in with GitHub.', category='error')
        return redirect(url_for("inscription"))
    user_info = github.get("/user")
    if user_info:
        session['loggedin'] = True
        session['username'] = user_info.get('name')
        session['avatar'] = user_info.get('avatar_url')
        session['login'] = user_info.get('login')
        session['location'] = user_info.get('location')
        session['email'] = user_info.get('email')

        flash('You were successfully logged in', category='success')
        return redirect(url_for('profile'))

    else:
        flash('error connecting and retreiving the data ')
        return redirect(url_for('inscription'))


@app.route('/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)

    # if not session['state'] == request.args['state']:
    #     abort(500)
    if 'state' not in session or not session['state'] == request.args.get('state', ''):
        abort(500)
    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(
        session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session['google_id'] = id_info.get('sub')
    session['name'] = id_info.get('name')
    session['email'] = id_info.get('email')
    session['picture'] = id_info.get('picture')

    return redirect('/protected_area')


@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
            # Create variables for easy access
            first_username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            _hashed_password = generate_password_hash(password)
            username = ' '.join(first_username.split())
            print("Original username:", first_username)
            username = ' '.join(first_username.split())
            print("Processed username:", username)
            cursor.execute(
                'SELECT * FROM public.geopovnet_auth WHERE username = %s', (username,))
            account = cursor.fetchone()
            print(account)
            if account:
                flash('Account already exists!')
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash('Invalid email address!')
            elif not re.match(r'^[A-Za-z ]+$', username):
                flash('fullname must contain only characters ans spaces!')
            elif len(username) < 3:
                flash('fullname should be at least 3 characters ')
            elif not username or not password or not email:
                flash('Please fill out the form!')
            else:
                # Account doesnt exists and the form data is valid, now insert new account into users table
                cursor.execute("INSERT INTO public.geopovnet_auth (username,password,hashed_password, email) VALUES (%s,%s,%s,%s)",
                               (username, password, _hashed_password, email))
                conn.commit()
#                 msh_template = """     
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Document</title>
# </head>
# <body>

# <h1></h1>

# <span>Bonjour !</span>

# <h4>Nous vous remercions d'utiliser Geopovnet !.</h4>

# <div>Geopovnet est une platforme geospatiale destinnée pour les pays en cours de développement.</div>

# <div>Nous voulons nous assurer qu'il s'agit bien de vous. Veuillez saisir le code de vérification suivant. 
# Si vous ne souhaitez pas créer un compte, ignorez cet e-mail.

# Geopovnet ne vous enverra jamais d'e-mail pour vous demander de communiquer ou de vérifier votre mot de passe, votre carte de crédit ou votre numéro de compte bancaire.
# </div>


# <div>Geopovnet,2023.  </div>
    
# </body>
# </html>
#     """
#                 msg = Message('Welcome togeopovnet! ',
#                               sender='noreply@geopovnet.com',
#                               recipients=['alayet.manel@gmail.com'])
#                 msg.html = render_template_string(msh_template)
#                 Mail.send(msg)
                flash('PArfait vous etes là !')
                # return render_template(url_for('connexion'))
        elif request.method == 'POST':
            flash('Remplir le formulaire!')
    except psycopg2.errors.UniqueViolation as e:
        error_msg = str(e).lower()
        conn.rollback()
        if 'email' in error_msg:
            flash("l'adresse courriel existe dans le serveur ! ")
        elif 'password' in error_msg:
            flash("le mot de passe existe dans le serveur ! ")
        elif 'username' in error_msg:
            flash(" Nom et Prénom existe dans le serveur ! ")
    return render_template('inscription.html')


@app.route('/supprimer', methods=['POST'])
def supprimer():
    if 'loggedin' not in session:
        flash('Veuillez se connecter avant ! ')
        return render_template('connexion.html')
    user_id = session.get('id')
    print(user_id)
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(
            'DELETE from public.geopovnet_auth WHERE id = %s', (user_id,))
        conn.commit()
    except Exception as e:
        flash("Erreur lors de la suppression du compte: " + str(e))
        return redirect(url_for('profile'))
    finally:
        cursor.close()
    session.pop('id', None)
    session.pop('loggedin', None)
    session.pop('username', None)
    flash('le compte supprimé avec succés !. ')
    return redirect(url_for('inscription'))


@ app.route('/connexion', methods=['POST', 'GET'])
def connexion():
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    except Exception as e:
        flash('Impossible de se connecter à la base de données.')
        return render_template('connexion.html')

    if request.method == 'POST':
        # Using .get() is safer than directly accessing the keys
        email = request.form.get('email')
        password = request.form.get('password')
        if not email or not password:
            flash("Aucun saisie!")
            return render_template('connexion.html')

        print(f" les coordonnes saisies sont  : {email} {password}")

        try:
            cursor.execute(
                'SELECT * FROM public.geopovnet_auth WHERE email = %s', (email,))
            compte = cursor.fetchone()
        except Exception as e:
            flash("Erreur lors de la récupération des informations de l'utilisateur.")
            return render_template('connexion.html')

        if compte:
            session['loggedin'] = True
            session['id'] = compte['id']
            session['email'] = compte['email']
            session['username'] = compte['username']
            session['password'] = compte['password']
            session['hashed_password'] = compte['hashed_password']

            return redirect(url_for('profile'))
        else:
            flash("Les données saisies sont éronnées ou n'existe pas dans le serveur !")

    return render_template('connexion.html')


@ app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'img/logo_geopovnet.svg', mimetype='image/vnd.microsoft.icon')


"""
steps : 



first lets start by delete account route  --- done 

after the store pass , username , email , probably only username and email 

store email  and password and id from both gmail and microsoft 

make sure to verify that the google auth variables exist or not in the db both goes for microsoft 

if yes flash ('user exists {email}' please put the correct password or click on forgot option )
else it is not in the db store it and login using the auth services  
--- partially i set the mal , username , password to unique and error msg if they already exisit in the db 
mainly the logic is like this if request.form['email'] is in db return error basically there is uniquevalidaor error when you add something that exisits already 
so if that error is true and email is the error trigger flash an error msg 

-- if the user creates an account send an email directly with a greeting -- pending 
Remove github auth --- 
github auth  --- done   
after the githyb authorized login  --redirect to the profile 

username that will take fullname instead so change regex to include only azAZ and split it to remove trailing spaces --- done 

"""


if __name__ == "__main__":
    app.run(debug=True, port=5000, host='geopovnet')
