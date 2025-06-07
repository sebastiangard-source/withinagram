from flask import Flask
from dotenv import load_dotenv
import os

from routes.main import main_bp

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default-secret-key")

app.register_blueprint(main_bp)

if __name__ == "__main__":
    app.run(debug=True)
