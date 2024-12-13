from flask import Flask, jsonify, request, abort, Blueprint
from middleware.auth import authenticate_token

library_bp = Blueprint("library", __name__)

# Register before_request function
@library_bp.before_request
def before_request():
    authenticate_token()

Books = [
    {"Title":"Bayn al-Qasrayn","Author": "Naguib Mahfouz", "Published Year":"1956", "ISBN": 9781},
    {"Title":"Thulathiyat al-Qahira","Author":"Naguib Mahfouz", "Published Year": "1957","ISBN":9782},
    {"Title":"Imarat Yaqubian","Author":"Alaa Al Aswany", "Published Year": "2002", "ISBN": 9783},
    {"Title":"Mudun al-Misriya","Author":"Hamada Ben-Amara", "Published Year": "2012", "ISBN": 9784}
]

# Retrieve all Books
@library_bp.route('/Books', methods=['GET'])
def get_Books():
    return jsonify(Books)

# Retrieve specific task by ISBN
@library_bp.route('/Books/<int:ISBN>', methods=['GET'])
def get_Book_by_ISBN(ISBN):
    for book in Books:
        if book['ISBN'] == ISBN:
            return jsonify(book)
    abort(404, description="Task not found")  # Handle not found

# Create a new Book
@library_bp.route('/Books', methods=['POST'])
def add_book():
    if not request.json or 'Title' not in request.json:
        abort(400, description="Invalid request")
    
    new_book = {
        'ISBN':Books[-1]['ISBN'] + 1,  # Increment ISBN based on the last book
        'Title': request.json['Title'],
        'Author': request.json.get('Author', ""),
        'Published Year':request.json.get('Published Year', "")
    }
    Books.append(new_book)
    return jsonify(new_book), 201

# Update a Book
@library_bp.route('/Books/<int:ISBN>', methods=['PUT'])
def update_Book(ISBN):
    if not request.json:
        abort(400, description="Invalid request: JSON body is required")

    for book in Books:
        if book['ISBN'] == ISBN:
            book['Title'] = request.json.get('Title', book['Title'])
            book['Author'] = request.json.get('Author', book['Author'])
            book['Published Year'] = request.json.get('Published Year', book['Published Year'])
            return jsonify(book)
    abort(404, description="Task not found")

# Search for books by author, published yea
@library_bp.route('/search', methods=['GET'])
def search():
    author = request.args.get('Author', None)
    published_year = request.args.get('Published Year', None)
    filtered_books = Books
    # Filter by author if provided
    if author:
        filtered_books = [book for book in filtered_books if author.lower() == book['Author'].lower()]
    # Filter by published year if provided
    if published_year:
        filtered_books = [book for book in filtered_books if book['Published Year'] == published_year]
    if filtered_books:
        return jsonify(filtered_books)
    else:
        return jsonify({"message": "No books found matching the criteria"}), 404

# Delete a Book
@library_bp.route('/Books/<int:ISBN>', methods=['DELETE'])
def delete_Book(ISBN):
    for book in Books:
        if book['ISBN'] == ISBN:
            Books.remove(book)
            return jsonify({"message": "Book got deleted"}), 200
    abort(404, description="Book not found")

# Initialize Flask app and register the blueprint
app = Flask(__name__)
app.register_blueprint(library_bp, url_prefix='/Books')
