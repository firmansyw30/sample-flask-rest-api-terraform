import os
from flask import Flask, jsonify, request
import uuid

app = Flask(__name__)

books = []  # In-memory storage for books

if __name__ == "__main__":
    app.run(debug=True) # Run the Flask app in debug mode
    port = int(os.environ.get("PORT", 8080)) 
    app.run(debug=True, host='0.0.0.0', port=port) # Note host 0.0.0.0

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to Flask API"})

def find_book(id):
    return next((book for book in books if book["id"] == id), None)

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify({"books": books})

@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = find_book(id)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    return jsonify({"book": book})

@app.route('/books', methods=['POST'])
def create_book():
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"message": "Invalid JSON input"}), 400

    next_id = max((b["id"] for b in books), default=-1) + 1
    book = {
        "id": next_id,
        "title": payload.get("title"),
        "author": payload.get("author")
    }
    books.append(book)
    return jsonify(book), 201

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = find_book(id)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    book["title"] = request.json.get("title", book["title"])
    book["author"] = request.json.get("author", book["author"])
    return jsonify({"book": book})

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    global books
    books = [book for book in books if book["id"] != id]
    return jsonify({"message": "Book deleted"})

@app.errorhandler(404)
def not_found(error):
    return jsonify({"message": "Route not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"message": "Internal server error"}), 500