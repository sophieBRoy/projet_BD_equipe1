from simplecrypt import encrypt, decrypt




if __name__=='__main__':
    password = 'sekret--up'
    message = 'this is a secret message'
    ciphertext = encrypt(password, message)
    print(ciphertext)
    print(decrypt('sekret', ciphertext))

