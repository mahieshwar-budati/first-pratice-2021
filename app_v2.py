import os
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite Database
db_path = os.path.join(app.root_path, "notes.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Note Database Model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=True, default="")
    content = db.Column(db.Text, nullable=True, default="")
    color = db.Column(db.String(50), nullable=False, default="bg-white")
    pinned = db.Column(db.Boolean, nullable=False, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "color": self.color,
            "pinned": self.pinned,
        }


# Initialize DB and seed initial data if empty
with app.app_context():
    db.create_all()
    if not Note.query.first():
        welcome_note = Note(
            title="Welcome to V2!",
            content=(
                "Try pinning, changing colors, searching, or editing this"
                " note! All changes now save to SQLite database."
            ),
            color="bg-yellow-100",
            pinned=True,
        )
        db.session.add(welcome_note)
        db.session.commit()


@app.route("/")
def index():
    return render_template("index_v2.html")


# API: Get all notes
@app.route("/api/notes", methods=["GET"])
def get_notes():
    notes = Note.query.order_by(Note.id.desc()).all()
    return jsonify([note.to_dict() for note in notes])


# API: Create note
@app.route("/api/notes", methods=["POST"])
def create_note():
    data = request.get_json() or {}
    new_note = Note(
        title=data.get("title", ""),
        content=data.get("content", ""),
        color=data.get("color", "bg-white"),
        pinned=data.get("pinned", False),
    )
    db.session.add(new_note)
    db.session.commit()
    return jsonify(new_note.to_dict()), 201


# API: Update note
@app.route("/api/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({"error": "Note not found"}), 404

    data = request.get_json() or {}
    if "title" in data:
        note.title = data["title"]
    if "content" in data:
        note.content = data["content"]
    if "color" in data:
        note.color = data["color"]
    if "pinned" in data:
        note.pinned = data["pinned"]

    db.session.commit()
    return jsonify(note.to_dict())


# API: Delete note
@app.route("/api/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({"error": "Note not found"}), 404

    db.session.delete(note)
    db.session.commit()
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True, port=5000)