# WELCOME TO MANICRYPT
* manicrypt is a simple and fun cryptography package
```
  pip intall manicrypt
```
## how to import?
```python
from manicrypt import mcrypt
```
>functions are

| Function | Description |
|----------|-------------|
|mencrypt(string,key)|encrypt the string with an key(integer)|
|mdecrypt(string,key)|decrypt the string with an key(integer)|
|imgwrite(img, msg)|hides the msg(message) into the img(picture) in binary|
|imgread(img)|display the hidden message img(picture) in binary|
|mapenc(string)|encrypt maps a value to srting|
|mapdec(string)|decrypt maps a value to string|

###sample

* __mencrypt()__
```python
from manicrypt import mcrypt
x = mcrypt.mencrypt('mani',2)
print(x)
```
>output
>'ocpk'

* __mdecrypt()__
```python
from manicrypt import mcrypt
x = mcrypt.mdecrypt('ocpk',2)
print(x)
```
>output
>'mani'

* __imgwrite()__
```python
from manicrypt import mcrypt
mcrypt.imgwrite('your image path or file_name.extention','your message')
```
* __imgread()__
```python
from manicrypt import mcrypt
mcrypt.imgread('your image path or file_name.extention')
```

* __mapenc()__
```python
from manicrypt import mcrypt
mcrypt.mapenc('your text')
```

* __mapdec()__
```python
from manicrypt import mcrypt
mcrypt.mapdec('your text')
```
