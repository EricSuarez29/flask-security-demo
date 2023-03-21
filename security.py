from flask_security import SQLAlchemyUserDatastore, Security
from models import Role, User
from db import db
 
security = Security()
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
