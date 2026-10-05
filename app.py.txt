from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# In-memory storage for notes
notes = [
    {
        "id": 1,
        "title": "Welcome!",
        "content": (
            "Try pinning, changing colors, searching, or editing this note!"
        ),
        "color": "bg-yellow-100",
        "pinned": True,
    }
]


@app.route("/")
def index():
    return render_template("index.html")


# API Route: Get all notes
@app.route("/api/notes", methods=["GET"])
def get_notes():
    return jsonify(notes)


# API Route: Create a note
@app.route("/api/notes", methods=["POST"])
def create_note():
    data = request.get_json()
    new_note = {
        "id": int(data.get("id", len(notes) + 1)),
        "title": data.get("title", ""),
        "content": data.get("content", ""),
        "color": data.get("color", "bg-white"),
        "pinned": data.get("pinned", False),
    }
    notes.insert(0, new_note)
    return jsonify(new_note), 201


# API Route: Update a note (Pin or Edit)
@app.route("/api/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    data = request.get_json()
    for note in notes:
        if note["id"] == note_id:
            note["title"] = data.get("title", note["title"])
            note["content"] = data.get("content", note["content"])
            note["color"] = data.get("color", note["color"])
            if "pinned" in data:
                note["pinned"] = data["pinned"]
            return jsonify(note)
    return jsonify({"error": "Note not found"}), 404


# API Route: Delete a note
@app.route("/api/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    global notes
    notes = [n for n in notes if n["id"] != note_id]
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True, port=5000)