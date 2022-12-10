""""
Password salting and hashing example
"""

import hashlib
import os


# import os  # << hint


def hash_pw(plain_text, salt='') -> str:
    """
    Generate hash of plain text. Here we allow for passing in a salt
    explicitly. This is so you can tinker and see the results.

    Python's Hashlib provides all we need here. Documentation is at
    https://docs.python.org/3/library/hashlib.html.

    Here we use SHA-1. (Weak!) For stronger encryption, see: bcrypt,
    scrypt, or Argon2. Nevertheless, this code should suffice for an
    introduction to some important concepts and practices.

    A few things to note.

    If we supply a fixed salt (or don't use a salt at all), then the
    output of the hash function becomes predictable -- for a given
    algorithm, the same password will always produce the same result.

    If we allow our algorithm to generate a salt from a pseudorandom
    input (e.g., using os.urandom(60)) then the same password will
    produce different results. All we know is the length of the combined
    salt and password.

    If we wish to be able to authenticate, then we must store the salt
    with the hash. We facilitate this by prepending the salt to the hash.

    :param plain_text: str (user-supplied password)
    :param salt: str
    :return: str (ASCII-encoded salt + hash)
    """
    salt = os.urandom(20).hex()

    hashable = salt + plain_text  # concatenate salt and plain_text
    hashable = hashable.encode('utf-8')  # convert to bytes
    this_hash = hashlib.sha1(hashable).hexdigest()  # hash w/ SHA-1 and hexdigest
    return salt + this_hash  # prepend hash and return


def authenticate(stored, plain_text, salt_length=None) -> bool:
    """
    Authenticate by comparing stored and new hashes.

    :param stored: str (salt + hash retrieved from database)
    :param plain_text: str (user-supplied password)
    :param salt_length: int
    :return: bool
    """
    salt_length = salt_length or 40  # set salt_length
    salt = stored[:salt_length]  # extract salt from stored value
    stored_hash = stored[salt_length:]  # extract hash from stored value
    hashable = salt + plain_text  # concatenate hash and plain text
    hashable = hashable.encode('utf-8')  # convert to bytes
    this_hash = hashlib.sha1(hashable).hexdigest()  # hash and digest
    return this_hash == stored_hash  # compare
