# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os

from sqlalchemy.pool import QueuePool

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Define the database - we are working with
# SQLite for this example
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 4

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"

CORS_HEADERS = 'Content-Type'

#Max upload size: 35MB
MAX_CONTENT_LENGTH = 35 * 1024 * 1024 

SQLALCHEMY_DB_AUTOCOMMIT = False

# Firebase Credentials
FIREBASE_CREDENTIALS = {
  #... add your credentials here
  # loaded by firebase_admin.credentials.Certificate(config:Dict)
}

