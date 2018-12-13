import hashlib

hash_object = hashlib.md5('Hello Wosdarld'.encode())

print(hash_object.hexdigest())
print(len(hash_object.hexdigest()))