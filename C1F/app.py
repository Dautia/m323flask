registered_users = [
    ('JohnDoe', 'john.doe@example.com'),
    ('AliceSmith', 'alice.smith@example.com'),
    ('BobJohnson', 'bob.johnson@example.com')
]


# Nach dem refactoring

# Funktion für die Konvertierung eines Strings in Großbuchstaben
def convert_to_upper(s):
    return s.upper()


# Funktion für die Konvertierung eines Benutzernamens
# und einer E-Mail-Adresse in einen formatierten String
def format_user_info(username, email):
    return f'Benutzer: {username}, E-Mail: {email}'


# Rekursive Funktion für die Binäre Suche nach Benutzern
def binary_search_users(username, low, high):
    if low > high:
        return -1
    mid = (low + high) // 2
    if username == registered_users[mid].username:
        return mid
    elif username > registered_users[mid].username:
        return binary_search_users(username, mid + 1, high)
    else:
        return binary_search_users(username, low, mid - 1)


# Vor dem refactoring
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
