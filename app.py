from flask import Flask
from dotenv import load_dotenv
from services.auth import auth_bp 
import os

from main import main_bp

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default-secret-key")

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True)
