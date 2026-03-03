from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory data store
items = [
    {"id": 1, "name": "Item One", "description": "First sample item"},
    {"id": 2, "name": "Item Two", "description": "Second sample item"},
]


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to the Flask API",
        "status": "running",
        "version": "1.0.0"
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/items", methods=["GET"])
def get_items():
    return jsonify({"items": items, "count": len(items)}), 200


@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = next((i for i in items if i["id"] == item_id), None)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200


@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Field 'name' is required"}), 400
    new_item = {
        "id": items[-1]["id"] + 1 if items else 1,
        "name": data["name"],
        "description": data.get("description", "")
    }
    items.append(new_item)
    return jsonify(new_item), 201


@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    global items
    item = next((i for i in items if i["id"] == item_id), None)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    items = [i for i in items if i["id"] != item_id]
    return jsonify({"message": f"Item {item_id} deleted"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
