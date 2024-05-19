import hashlib


def handle(senha):
    sha256 = hashlib.sha256()
    sha256.update(senha.encode('utf-8'))
    return sha256.hexdigest() 