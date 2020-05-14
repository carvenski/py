import base64


"""RC4 algorithm, RC4's encode and decode use the same func"""
def RC4(data, key):
    x = 0
    box = range(256)
    for i in range(256):
        x = (x + box[i] + ord(key[i % len(key)])) % 256
        box[i], box[x] = box[x], box[i]
    x = y = 0
    out = []
    for char in data:
        x = (x + 1) % 256
        y = (y + box[x]) % 256
        box[x], box[y] = box[y], box[x]
        out.append(chr(ord(char) ^ box[(box[x] + box[y]) % 256]))
    return ''.join(out)

def RC4encode(data, key):
    return RC4(data, key)

def RC4decode(data, key):
    return RC4(data, key)


# test
print('base64+RC4 -> %s' % base64.b64encode(  RC4encode('test', 'key') ) )

print( 'RC4 encode -> %s' %   RC4encode('test','key')  )
print( 'RC4 decode -> %s' %   RC4decode( RC4encode('test','key'), 'key')  )




