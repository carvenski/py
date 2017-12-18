from django.utils.crypto import (pbkdf2, get_random_string)

import hashlib

password = '1990724'
algorithm = "pbkdf2_sha256"
iterations = 24000
salt = 'FkZPjKAA1v1R'
digest = hashlib.sha256
hash = pbkdf2(password, salt, iterations, digest=digest)
hash = hash.encode('base64').strip()
print "%s$%d$%s$%s" % (algorithm, iterations, salt, hash)