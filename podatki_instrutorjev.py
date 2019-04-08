import requests
import re
import urllib3
import matplotlib.pyplot as plt
import matplotlib.image as img
from math import *
from PIL import Image
from io import BytesIO

page = requests.get('https://www.go-tel.si/instrukcije/instruktorji.php').text
tabela = re.split(r'<div class="cleared"></div>', page)[2]
instruktorji = re.split(r'<div class="instruktor_area insOkvir"', tabela)

f = open("instruktorji.txt", 'x')
i = 1
for s in instruktorji:
    vrstica = re.findall(r'class="nondecor">\w+\s*</a>', s)
    if len(vrstica) == 0: continue
    ime = re.match(r'class="nondecor">(\w+)\s*</a>', vrstica[0]).group(1)
    podatki = re.search(r'.*razpolozljivost="(\d+)".*reference="(\d+)".*razdalja="(\d+)".*starost="(\d+)".*href="(\d+)-(\w+)".*src="images/Instruktor(\w+).(\w+)".*', s, re.S)
    if podatki is None: continue
    razpolozljivost = podatki.group(1)
    reference = podatki.group(2)
    razdalja = podatki.group(3)
    starost = podatki.group(4)
    koda = podatki.group(5)+'-'+podatki.group(6)
    urlslika = 'images/Instruktor'+podatki.group(7)+'.'+podatki.group(8)
    #slika = requests.get('https://www.go-tel.si/instrukcije/'+urlslika).text

    '''Za vsazga instruktorja posebi'''
    instr = requests.get('https://www.go-tel.si/instrukcije/'+ koda).text
    cenapod = re.search(r'.*onchange="cena\(\'(\d+)\'\).*', instr)
    cena = cenapod.group(1)
    krajpod = re.search(r'.*naslov=".+, (.+)"', instr)
    kraj = krajpod.group(1)
    urepod = re.search(r'.*<p>(\d+) ur</p>.*', instr)
    ure = urepod.group(1)
    ucencipod = re.search(r'.*<p>(\d+)\+.*', instr)
    ucenci = ucencipod.group(1)
    predmetipod = re.search(r'.*content=.+predmetov\:(.+)Individualno.*', instr)
    predmetipod1 = predmetipod.group(1)
    predmeti = []
    
    if 'v krajih' in predmetipod1:
        pred, _ = predmetipod1.split('v krajih')
    else:
        pred = predmetipod1
    pred = pred.strip()

    predmeti = pred.split(', ')
    
    f = open('instruktorji.txt', 'a')
    f.write(ime+'-'+kraj+'-'+str(predmeti)+'-'+reference+'-'+razpolozljivost+'-'+ucenci+'-'+ure+'\n')
    f.close

    
##    img = open('instruktor'+str(i)+'.png', 'wb')
##    img.write(slika)
    with open('instruktor'+str(i)+'.png', 'wb') as handle:
        response = requests.get('https://www.go-tel.si/instrukcije/'+urlslika, stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)
    i += 1

    
