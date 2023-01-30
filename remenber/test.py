import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
import easyocr

reader = easyocr.Reader(['ko', 'en'])
with open('C:\\Users\\admin\\Desktop\\캡처.PNG','rb') as pf:
    img = pf.read()
    result = reader.readtext(img)
    for res in result:
        print(res)
        
print(res[:-2])

