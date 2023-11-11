from flask import Flask, request, jsonify

app = Flask(__name__)


# Klasse mit immutable values für Benutzerdaten
class User:
    def __init__(self, username, email):
        self._username = username
        self._email = email

    @property
    def username(self):
        return self._username

    @property
    def email(self):
        return self._email

    def __repr__(self):
        return f"User({self._username}, {self._email})"


# Liste für registrierte Benutzer
registered_users = [
    User('JohnDoe', 'john.doe@example.com'),
    User('AliceSmith', 'alice.smith@example.com')
]

# Benutzerregistrierung
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    username = data['username']
    email = data['email']

    new_user = User(username, email)

    # Verwendung von immutable values für Benutzerdaten
    registered_users.append(new_user)

    return jsonify({'message': 'Benutzer erfolgreich registriert'}), 201


# Anzeige registrierter Benutzer (nur zum Nachweis, nicht in produktivem Code verwenden)
@app.route('/users', methods=['GET'])
def get_users():
    user_list = [{'username': user.username, 'email': user.email} for user in registered_users]
    return jsonify({'users': user_list})


if __name__ == '__main__':
    app.run(debug=True)
