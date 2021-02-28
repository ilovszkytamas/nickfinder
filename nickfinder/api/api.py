from flask import Flask, jsonify, request, session
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
import jwt
from datetime import datetime, timedelta


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/nickfinder'
db = SQLAlchemy(app)
CORS(app, resources={r"/.*": {"origins": "*"}})
app.config['SECRET_KEY'] = 'secretkey'
app.config['CORS_HEADERS'] = 'Content-Type'


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40))
    email = db.Column(db.String(40))
    password = db.Column(db.String(40))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


@app.route('/')
#@cross_origin()
def index():
    return " szevasz"

@app.route('/register', methods=['POST'])
#@cross_origin()
def registerUser():
    user = users(request.json["username"],request.json["email"], request.json["password"])
    exists = users.query.filter_by(username=user.username).first()
    if exists is None:
        db.session.add(user)
        db.session.commit()
        return jsonify(message="success")
    else:
        return jsonify(message="userexists")

@app.route('/login', methods=['POST'])
#@cross_origin()
def loginUser():
    username = request.json["username"]
    password = request.json["password"]
    exists = users.query.filter_by(username=username, password=password).first()
    if exists is None:
        return jsonify(message="notfound")
    else: 
        payload = {
            'username' : exists.username,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }
        jwt_token = jwt.encode(payload, app.config['SECRET_KEY'])
        return jsonify({
            'message': "success",
            'token': jwt_token
        })


if __name__ == '__main__':
    app.run(debug=True)

    