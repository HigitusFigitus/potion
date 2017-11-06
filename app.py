from flask import Flask, request, json, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///potions.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Potion(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  potion_name = db.Column(db.String(64), unique=True)
  potion_type = db.Column(db.String())
  potion_class = db.Column(db.String())

  def __init__(self, potion_name, potion_type, potion_class):
    self.potion_name = potion_name
    self.potion_type = potion_type
    self.potion_class = potion_class

  def toJSON(self):
    return {"potion_name": self.potion_name,
            "potion_type": self.potion_type,
            "potion_class": self.potion_class,
            "location": "/api/v1/potions/{}".format(self.potion_name)}

if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=5000)