import hashlib

def encrypt_string(the_string):
    sha_signature = hashlib.sha256(the_string.encode()).hexdigest()
    return sha_signature
