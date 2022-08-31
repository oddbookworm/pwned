import hashlib
import lastpass
import requests

passwords = []

def usingLastPass():
    global passwords

    print('LastPass username: ')
    username = input()
    print('LastPass password: ')
    password = input()

    vault = lastpass.Vault.open_remote(username, password)
    for i in vault.accounts:
        if i.password != b'':
            passwords.append(i.password)

while True:
    print('Do you use LastPass and would like to check your LastPass passwords? (y/n)')
    answer = input()
    if answer == 'y':
        usingLastPass()
        break
    elif answer == 'n':
        break
    else:
        print('I\'m not sure what you meant to type')

while True:
    print('Type password, then press Enter. If you don\'t want to enter another, just press Enter.')
    newPassword = input()
    if newPassword == '':
        break
    else:
        passwords.append(newPassword.encode('utf8'))

# passwords = [password.encode('utf8') for password in passwords if type(password) == str]

# temp = []
# for value in passwords:
#     if type(value) != bytes:
#         temp.append(value.encode('utf8'))
#     else:
#         temp.append(value)

passwords = list(set(passwords))

hashes = [hashlib.sha1(value) for value in passwords]
hashes = [value.hexdigest() for value in hashes]

firstFives = [value[0:5] for value in hashes]

links = ['https://api.pwnedpasswords.com/range/' + value for value in firstFives]

foundHashes = {}
for link in links:
    r = requests.get(link)
    lines = r.text.replace('\r', '').split('\n')
    for line in lines:
        temp = line.split(':')
        foundHashes.update({temp[0].lower() : temp[1]})

def getPw(hash, hashList, pwList):
    index = 0
    while True:
        if hashList[index] == hash:
            break
        else:
            index += 1
    
    return pwList[index].decode()

keys = list(foundHashes.keys())
for value in hashes:
    length = len(value)
    if value.lower()[5: length] in keys:
        pw = getPw(value, hashes, passwords)
        print(pw + ' found ' + foundHashes[value.lower()[5: length]] + ' times')

print('\nPress any key to exit the program')
while True:
    temp = input()
    break
