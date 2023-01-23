# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os

from sqlalchemy.pool import QueuePool

SERVER_ENDPOINT = '127.0.0.1'
SERVER_PORT     = '5432'

DB_NAME = 'database_name'
DB_USER = 'database_user'
DB_PSWD = 'password'


BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Define the database - we are working with
# SQLite for this example
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PSWD}@{SERVER_ENDPOINT}:{SERVER_PORT}/{DB_NAME}"
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

#Max upload size: 5MB
MAX_CONTENT_LENGTH = 5 * 1024 * 1024 

# Fix bug with flask_sqlalchemy. Increase the default pool_size
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 20,
    'pool_recycle': 120,
    'pool_pre_ping': True,
    'pool_recycle': 120,
}

SQLALCHEMY_DB_AUTOCOMMIT = True

# Firebase Credentials
FIREBASE_CREDENTIALS = {
  #... add your credentials here
  # loaded by firebase_admin.credentials.Certificate(config:Dict)
}

# Sample: *TO CHANGE*
AWS_ACCESS_KEY_ID = 'XXXXXXXXXXXXXXXXXXXX'
AWS_SECRET_ACCESS_KEY = "XXXXXXXXXXXXXXXXXXXX"
AWS_REGION = 'eu-west-1'

os.environ['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY_ID
os.environ['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY
os.environ['AWS_REGION'] = AWS_REGION

DYNAMO_TABLES = [
    dict(
            TableName='private_messages',
            KeySchema=[dict(AttributeName='id', KeyType='HASH')],
            GlobalSecondaryIndexes=[
                dict(IndexName='index-sender',
                     KeySchema=[
                        dict(AttributeName='sender', KeyType='HASH'),
                     ],
                     Projection=dict(ProjectionType='ALL'),
                     ProvisionedThroughput=dict(ReadCapacityUnits=5, WriteCapacityUnits=5)
                ),
                dict(IndexName='index-destination',
                     KeySchema=[
                        dict(AttributeName='destination', KeyType='HASH'),
                     ],
                     Projection=dict(ProjectionType='ALL'),
                     ProvisionedThroughput=dict(ReadCapacityUnits=5, WriteCapacityUnits=5)
                )
            ],
            AttributeDefinitions=[
                dict(AttributeName='id', AttributeType='S'),
                dict(AttributeName='sender', AttributeType='S'),
                dict(AttributeName='destination', AttributeType='S'),

            ],
            ProvisionedThroughput=dict(ReadCapacityUnits=5, WriteCapacityUnits=5),
            
        )
]

