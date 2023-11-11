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

# Binäre Suche für Benutzername in der registrierten Benutzerliste
def binary_search_users(username):
    low, high = 0, len(registered_users) - 1

    while low <= high:
        mid = (low + high) // 2
        current_username = registered_users[mid].username

        if current_username == username:
            return mid
        elif current_username < username:
            low = mid + 1
        else:
            high = mid - 1

    return -1  # Benutzer nicht gefunden

# Benutzerregistrierung mit binärer Suche
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    username = data['username']
    email = data['email']

    # Binäre Suche, ob der Benutzer bereits registriert ist
    existing_user_index = binary_search_users(username)

    if existing_user_index != -1:
        return jsonify({'message': 'Benutzer existiert bereits'}), 409

    new_user = User(username, email)
    registered_users.append(new_user)

    return jsonify({'message': 'Benutzer erfolgreich registriert'}), 201

@app.route('/users', methods=['GET'])
def get_users():
    user_list = [{'username': user.username, 'email': user.email} for user in registered_users]
    return jsonify({'users': user_list})

if __name__ == '__main__':
    app.run(debug=True)
