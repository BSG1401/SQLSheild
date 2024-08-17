from flask import Flask

app = Flask(__name__)

# Set the secret key for session management
app.config['SECRET_KEY'] = '73K9J4D2F8H5G6Y1QWE0R5P7'

from app import routes
