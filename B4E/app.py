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
    User('AliceSmith', 'alice.smith@example.com'),
    User('BobJohnson', 'bob.johnson@example.com')
]

# Lambda-Ausdruck für die Konvertierung eines Strings in Großbuchstaben
convert_to_upper = lambda s: s.upper()

# Lambda-Ausdruck für die Konvertierung eines Benutzernamens
# und einer E-Mail-Adresse in einen formatierten String
format_user_info = lambda username, email: f'Benutzer: {username}, E-Mail: {email}'

# Binäre Suche für Benutzer
binary_search_users = lambda username, low, high: (
    lambda u, l, h: -1 if l > h else (h - l) // 2 if u == registered_users[
        (l + h) // 2].username else binary_search_users(u, (l + h) // 2 + 1, h) if u > registered_users[
        (l + h) // 2].username else binary_search_users(u, l, (l + h) // 2 - 1))(username, low, high)


# Beispiel: Anwendung von map, filter und reduce
@app.route('/process_users', methods=['GET'])
def process_users():
    # Anwendung von map, filter und reduce auf die registrierten Benutzer
    uppercase_usernames = list(map(lambda user: {'username': user.username.upper(), 'email': user.email},
                                   registered_users))

    filtered_users = list(filter(lambda user: user['username'].startswith('A'), uppercase_usernames))

    concatenated_emails = reduce(lambda acc, user: acc + user['email'] + ', ', filtered_users, '')

    return jsonify({'processed_users': filtered_users, 'concatenated_emails': concatenated_emails})


# Benutzerregistrierung mit Binärer Suche und Lambda-Ausdrücken
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
