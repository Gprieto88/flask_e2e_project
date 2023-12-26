from flask import flask, render_template, request, url_for, redirect, session
import pandas as pd
from flask_session import session
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token
from oauth.db_functions import update_or_create_user
import os
from dotenv import load_dotenv
from pandas import read_sql
from sqlalchemy import create_engine, text

app = Flask(__name__)


app.secret_key = os.urandom(12)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
oauth = OAuth(app)


# Database connection settings from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = int(os.getenv("DB_PORT", 3306))




# Connection string
conn_string = (
    f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
)
engine = create_engine(conn_string, echo=False)


## Connection settings for the Google OAuth
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')


@app.route("/")

app.secret_key = os.urandom(12)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
oauth = OAuth(app)


# Database connection settings from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = int(os.getenv("DB_PORT", 3306))




# Connection string
conn_string = (
    f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
)
engine = create_engine(conn_string, echo=False)


## Connection settings for the Google OAuth
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')


@app.route("/")
def index():
    try:
        logging.debug("You have successfully accessed the index page!")
        return render_template('index.html')
    except Exception as e:
        logging.error(f"an error occurred! {e}")
        return "Please try again!"


@app.route('/login/')
def google():
    return render_template('google_login.html')


@app.route('/login/google/')
def login():
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )


    # Redirect to google_auth function
    redirect_uri = url_for('google_auth', _external=True)
    print('REDIRECT URL: ', redirect_uri)
    session['nonce'] = generate_token()
    redirect_uri = 
'https://5000-cs-174475239264-default.cs-us-east1-vpcf.cloudshell.dev/google/auth/'
    return oauth.google.authorize_redirect(redirect_uri, nonce=session['nonce'])


@app.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token, nonce=session['nonce'])
    session['user'] = user
    update_or_create_user(user)
    print(" Google User ", user)
    return redirect('/dashboard')


@app.route('/dashboard/')
def dashboard():
    user = session.get('user')
    if user:
        return render_template('dashboard.html', user=user)
    else:
        return redirect('/')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')
   
@app.route('/DATANAME')
def Covid19DailyCases():
    with engine.connect() as connection:
        query = text('SELECT * FROM Covid19DailyCases’)
        result = connection.execute(query)
        db_data = result.fetchall()
    return render_template('Covid19DailyCases.html', data=db_data)


@app.route("/error")
def error():
    try:
