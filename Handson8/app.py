from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample data - in a real application, this would be a database
items = [
    {"id": 1, "name": "Item 1", "description": "Description for Item 1"},
    {"id": 2, "name": "Item 2", "description": "Description for Item 2"}
]


# Helper function to find an item by ID
def find_item(item_id):
    for item in items:
        if item["id"] == item_id:
            return item
    return None


@app.route('/api/items', methods=['GET'])
def get_items():
    """Get all items or filter by query parameters"""
    # Handle query parameters (optional)
    name_filter = request.args.get('name')
    if name_filter:
        filtered_items = [item for item in items if name_filter.lower() in item['name'].lower()]
        return jsonify(filtered_items)
    return jsonify(items)


@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Get a specific item by ID"""
    item = find_item(item_id)
    if item:
        return jsonify(item)
    return jsonify({"error": "Item not found"}), 404


@app.route('/api/items', methods=['POST'])
def create_item():
    """Create a new item"""
    data = request.get_json()

    # Validate request data
    if not data or not 'name' in data:
        return jsonify({"error": "Name is required"}), 400

    # Generate a new ID (in a real app, the database would handle this)
    new_id = max(item["id"] for item in items) + 1 if items else 1

    # Create new item
    new_item = {
        "id": new_id,
        "name": data["name"],
        "description": data.get("description", "")
    }

    # Add to our "database"
    items.append(new_item)

    return jsonify(new_item), 201


@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """Update an existing item"""
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Update item fields
    if 'name' in data:
        item['name'] = data['name']
    if 'description' in data:
        item['description'] = data['description']

    return jsonify(item)


@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete an item"""
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    # Remove from our "database"
    items.remove(item)

    return jsonify({"message": f"Item {item_id} deleted successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)