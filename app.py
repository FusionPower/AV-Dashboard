from flask import Flask
from user_routes import user_routes
from extensions import db, bcrypt
from simulation_routes import simulation_routes

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
app.config["SECRET_KEY"] = "sample_dummy_secret_key"

# Initialize db and bcrypt
db.init_app(app)
bcrypt.init_app(app)

# Register blueprints
app.register_blueprint(user_routes)
app.register_blueprint(simulation_routes)
