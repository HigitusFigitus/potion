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


import validations
@app.route("/api/v1/potions", methods=["GET", "POST"])
def potions():
    if request.method == "POST":
        if request.headers.get("Authorization") != "admin":
            return jsonify({"error": "Invalid credentials"}), 401

        request_to_json = request.get_json(force=True)
        potion_name = request_to_json.get("potion_name", "")
        potion_type = request_to_json.get("potion_type", "")
        potion_class = request_to_json.get("potion_class", "")

        try:
            validations.validate_potion(potion_name, potion_type, potion_class)
        except validations.InvalidPotionError as e:
            return jsonify({"error": str(e)}), 400

        new_potion = Potion(potion_name, potion_type, potion_class)
        db.session.add(new_potion)
        db.session.commit()
        created_potion = json.dumps(new_potion.toJSON())
        return created_potion, 201

    else:
        p_filter = request.args
        if "potion_type" in p_filter and p_filter["potion_type"] in (
                                                          "passive", "active"):
            potions = Potion.query.filter_by(
                potion_type=p_filter["potion_type"]).all()

        elif "potion_class" in p_filter and p_filter["potion_class"] in (
                                             "life", "mana", "fire", "poison"):
            potions = Potion.query.filter_by(
                potion_class=p_filter["potion_class"]).all()
        else:
            potions = Potion.query.all()

            json_potions = json.dumps([p.toJSON() for p in potions])
        return json_potions, 200


@app.route("/api/v1/potions/<potion_name>", methods=["GET"])
def potion(potion_name):
    requested_potion = Potion.query.filter_by(potion_name=potion_name).first()
    if requested_potion:
        json_potion = json.dumps(requested_potion.toJSON())
        return json_potion, 200
    else:
        return jsonify({"error": "The requested potion doesn't exist"}), 404


if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=5000)
