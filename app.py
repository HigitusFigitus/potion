from flask import Flask, request, json, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///potions.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=5000)