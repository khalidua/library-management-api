from flask import Flask, jsonify, send_from_directory
from routes.library import library_bp
import json
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.register_blueprint(library_bp, url_prefix="/library")

swagger_json_url = '/static/swagger.yaml'

swagger_ui_blueprint = get_swaggerui_blueprint(
    '/api-docs',
    swagger_json_url,
    config={'app_name': "Flask API Testing"}
)

app.register_blueprint(swagger_ui_blueprint, url_prefix='/api-docs')

@app.route('/static/swagger.json')
def serve_swagger_json():
    return send_from_directory('static', 'swagger.yaml')

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Todo API!"})

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404

if __name__ == "__main__":
    app.run(port=3000)
