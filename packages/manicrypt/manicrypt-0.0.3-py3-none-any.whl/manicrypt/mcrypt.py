# functions for simple char shift encription
def mencrypt(string,key):
    enc = ''
    for letter in string:
        encletter = chr(ord(letter)+int(key))
        enc += encletter
    return enc

def mdecrypt(string,key):
    enc = ''
    for letter in string:
        encletter = chr(ord(letter)-int(key))
        enc += encletter
    return enc

# function for simple message attach to the image
def imgwrite(img, msg):
    with open(img, 'ab') as f:
        encoded_msg = msg.encode('utf-8')
        data = b" " + encoded_msg
        f.write(data)

def imgread(img):
    with open(img, 'rb') as f:
        print(f.read())


#function for the greek encryption and decryption
setin = {'À':'A','Á':'B','Â':'C','Ã':'D','Ä':'E','Ç':'F','È':'G','É':'H','Ê':'I','Ë':'J','Ì':'K','Í':'L','Î':'M','Ï':'N','Ð':'O','Ñ':'P','Ò':'Q','Ó':'R','Ô':'S','Õ':'T','Ö':'U','Ø':'V','Ù':'W','Ú':'X','Û':'Y','Ü':'Z','Ý':' ','á':'a','â':'b','ã':'c','ä':'d','å':'e','ý':'f','ç':'g','è':'h','é':'i','ê':'j','ë':'k','ì':'l','í':'m','î':'n','ï':'o','ð':'p','ñ':'q','ò':'r','ó':'s','ô':'t','õ':'u','ö':'v','ü':'w','ø':'x','ù':'y','ú':'z'}
def mapenc(string):
    for x in string:
        for z,y in setin.items():
            if x == y:
                print(z,end='')
    print('')
    
def mapdec(string):
    for x in string:
        for z,y in setin.items():
            if x == z:
                print(y,end='')
    print('')
