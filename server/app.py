# server/app.py

from flask import Flask, jsonify
from models import db, Earthquake

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

db.init_app(app)


# ✅ CREATE TABLES + SEED DATA (THIS IS THE MISSING PIECE)
with app.app_context():
    db.create_all()

    if Earthquake.query.count() == 0:
        earthquakes = [
            Earthquake(magnitude=9.5, location="Chile", year=1960),
            Earthquake(magnitude=9.2, location="Alaska", year=1964),
            Earthquake(magnitude=9.1, location="Sumatra", year=2004),
            Earthquake(magnitude=8.8, location="Chile", year=2010),
            Earthquake(magnitude=8.6, location="Sumatra", year=2012),
        ]
        db.session.add_all(earthquakes)
        db.session.commit()


@app.route("/earthquakes/<int:id>")
def get_earthquake(id):
    quake = Earthquake.query.filter_by(id=id).first()

    if quake:
        return jsonify(quake.to_dict()), 200
    else:
        return jsonify({"message": f"Earthquake {id} not found."}), 404


@app.route("/earthquakes/magnitude/<float:magnitude>")
def earthquakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(
        Earthquake.magnitude >= magnitude
    ).all()

    return jsonify({
        "count": len(quakes),
        "quakes": [q.to_dict() for q in quakes]
    }), 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)
