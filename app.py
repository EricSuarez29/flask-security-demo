from flask import Flask, url_for
from flask_security import Security, SQLAlchemyUserDatastore, roles_required
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.sql.base import roles
from db import db
from models import Product, User, Role, roles_users
from security import security, user_datastore
from resources.main import blp as main_blueprint
from resources.auth import blp as auth_blueprint, generate_password_hash
from admin import StoreModelView

app = Flask(__name__)
app.config["SECRET_KEY"] = "thisisasecret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["FLASK_ADMIN_SWATCH"] = "cerulean"

admin = Admin(app, name="store", template_mode="bootstrap4")
admin.add_view(StoreModelView(User, db.session))
admin.add_view(StoreModelView(Role, db.session))
admin.add_view(StoreModelView(Product, db.session))


db.init_app(app)


@app.before_first_request
def restrict_admin_url():
    endpoint = "admin.index"
    url = url_for(endpoint)
    admin_index = app.view_functions.pop(endpoint)

    @app.route(url, endpoint=endpoint)
    @roles_required("admin")
    def secure_admin_index():
        return admin_index()


@app.before_first_request
def init():
    db.create_all()

    role = Role(name="admin", description="admin role")
    if not Role.query.filter_by(name="admin").first():
        db.session.add(role)

    if not User.query.filter_by(email="admin@admin.com").first():
        user_datastore.create_user(
            name="Admin",
            email="admin@admin.com",
            password=generate_password_hash("admin", method="sha256"),
            roles=[role],
        )
    db.session.commit()


app.register_blueprint(main_blueprint)
app.register_blueprint(auth_blueprint)

security.init_app(app, user_datastore)
