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


# Funktion für binäre Suche in der registrierten Benutzerliste
def binary_search_users(username, low, high):
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


# Lambda-Ausdruck für die Konvertierung eines Strings in Großbuchstaben
convert_to_upper = lambda s: s.upper()

# Lambda-Ausdruck für die Konvertierung eines Benutzernamens
# und einer E-Mail-Adresse in einen formatierten String
format_user_info = lambda username, email: f'Benutzer: {username}, E-Mail: {email}'


# Funktion für Benutzerregistrierung mit Binärer Suche und Lambda-Ausdrücken
def register_user_with_binary_search_and_format(username, email, search_function, format_function):
    existing_user_index = search_function(username, 0, len(registered_users) - 1)

    if existing_user_index != -1:
        return {'message': 'Benutzer existiert bereits'}, 409

    new_user = User(username, email)
    registered_users.append(new_user)

    formatted_info = format_function(username, email)
    return {'message': f'Benutzer erfolgreich registriert. {formatted_info}'}, 201


# Benutzerregistrierung mit Binärer Suche und Lambda-Ausdrücken
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username, email = data['username'], data['email']

    # Anwendung der Lambda-Ausdrücke für die Großschreibung des Benutzernamens und die Formatierung der Benutzerinfo
    response, status_code = register_user_with_binary_search_and_format(username, email, binary_search_users,
                                                                        format_user_info)
    return jsonify(response), status_code


# Anzeige registrierter Benutzer (nur zum Nachweis, nicht in produktivem Code verwenden)
@app.route('/users', methods=['GET'])
def get_users():
    user_list = [{'username': user.username, 'email': user.email} for user in registered_users]
    return jsonify({'users': user_list})


if __name__ == '__main__':
    app.run(debug=True)
