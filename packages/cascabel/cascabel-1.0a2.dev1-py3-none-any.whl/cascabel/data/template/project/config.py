import pathlib, os
from flask import Flask
from dotenv import load_dotenv

load_dotenv(f"{pathlib.Path(__file__).parent.absolute()}/.env")

app = Flask("my_app")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = os.getenv("SECRET_KEY")