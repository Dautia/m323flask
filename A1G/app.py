from flask import Flask, request, jsonify
from hashlib import sha256

app = Flask(__name__)


def encrypt_password(password):
    # Pure function für die Verschlüsselung des Passworts
    return sha256(password.encode()).hexdigest()


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    encrypted_password = encrypt_password(password)
    user_data = {'username': username, 'password': encrypted_password}
    return jsonify({'message': 'Registration successful!', 'user': user_data})
