from flask import Flask,request,jsonify
app = Flask(__name__)

TOKEN="mysecrettoken"

def authenticate_token():
    token= request.headers.get("Authorization")
    if not token or token !=f"Bearer {TOKEN}":
        return jsonify({"error":"unauthorized"}),401