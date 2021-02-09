import sys

def decrypt(text):
    result = ""

    for i in range(len(text)):
        char = text[i]

        if (char.isupper()):
            result += chr((ord(char) + 16 - 65) % 26 + 65)

        elif(char.islower()):
            result += chr((ord(char) + 16 - 97) % 26 + 97)

        else:
            result += char

    return result


if len(sys.argv) != 2:
    print("Usage decrypter.py *.txt")
    exit()

encryptedFile = open(sys.argv[1], 'r', encoding = 'utf-8', errors = 'ignore')
decryptedFile = open('Decrypted Data.txt', 'a',encoding = 'utf-8', errors = 'ignore')

for line in encryptedFile:
    decryptedFile.write(decrypt(line))

encryptedFile.close()
decryptedFile.close()
