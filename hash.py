import hashlib

hash_object = hashlib.md5('Hello Wosdarld'.encode())

print(hash_object.hexdigest())
print(len(hash_object.hexdigest()))

print(len('D:\\3- DSA\\Project\\simple\\articles\\a\\l\\b\\Image~Albert_Camus,_gagnant_de_prix_Nobel,_portrait_en_buste,_posÃ©_au_bureau,_faisant_face_Ã _gauche,_cigarette_de_tabagisme.jpg_476e.html'))