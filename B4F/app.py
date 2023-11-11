from flask import Flask, request, jsonify
from functools import reduce

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


# Funktion für die Kombination von Map, Filter und Reduce zur Verarbeitung von Benutzerdaten
@app.route('/process_users', methods=['GET'])
def process_users():
    # Anwendung von Map: Konvertiere Benutzernamen zu Großbuchstaben
    uppercase_usernames = map(lambda user: user.username.upper(), registered_users)

    # Anwendung von Filter: Filtere Benutzer mit Länge des Benutzernamens größer als 5
    filtered_users = filter(lambda user: len(user.username) > 5, registered_users)

    # Anwendung von Reduce: Kombiniere E-Mail-Adressen zu einem einzelnen String
    combined_emails = reduce(lambda acc, user: f"{acc}, {user.email}", filtered_users, "")

    return jsonify({
        'uppercase_usernames': list(uppercase_usernames),
        'filtered_users': [{'username': user.username, 'email': user.email} for user in filtered_users],
        'combined_emails': combined_emails[2:]  # Entferne das anfängliche ", "
    })


# Benutzerregistrierung mit binärer Suche und Lambda-Ausdrücken
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username, email = data['username'], data['email']

    existing_user_index = binary_search_users(username, 0, len(registered_users) - 1)

    if existing_user_index != -1:
        return {'message': 'Benutzer existiert bereits'}, 409

    new_user = User(username, email)
    registered_users.append(new_user)

    formatted_info = format_user_info(username, email)
    return {'message': f'Benutzer erfolgreich registriert. {formatted_info}'}, 201


# Anzeige registrierter Benutzer (nur zum Nachweis, nicht in produktivem Code verwenden)
@app.route('/users', methods=['GET'])
def get_users():
    user_list = [{'username': user.username, 'email': user.email} for user in registered_users]
    return jsonify({'users': user_list})


if __name__ == '__main__':
    app.run(debug=True)
