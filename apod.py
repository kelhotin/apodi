import requests
import json
import os
import datetime
from PIL import Image
from io import BytesIO
import subprocess
from pathlib import Path


##Palauttaa mappina resoluution, jotta kuva saadaan oikean kokoiseksi
def getScreenResolution():
    out = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4',shell=True, stdout=subprocess.PIPE).communicate()[0]
    res = out.split()[0].split(b'x')
    return {'w': res[0], 'h': res[1]}


#Hakee apodin json-filen, sisaan params jossa on parametrit mappina, requests osaa kivasti kasitella niin ei tarvi pohtia..
def getAPODData(params):
    print('Fetching data from api.nasa.gov...')
    res = requests.get('https://api.nasa.gov/planetary/apod', params=params)
    data = res.json()
    with open('data.json', 'w') as f:
        json.dump(data, f)

    return data

#Hakee APODin
def getAPOD(params):
    data = getAPODData(params)
    imgUrl = data["hdurl"]
    print('Fetching APOD')
    img = Image.open(BytesIO(requests.get(imgUrl).content))
    return img, data

def setWallpaper(img):
    m = getScreenResolution()
    w = int(m['w'])
    h = int(m['h'])
    img1 = img.resize((w, h))
    img.save('pic.jpg')
    com = "gsettings set org.gnome.desktop.background picture-uri \'file://" + (os.path.abspath('pic.jpg') + "\'")
    os.system(com)
    
#APIkeyta yms
if __name__=='__main__':

    #TODO, tarkista onko kyseisen paivan apodi jo ladattu
    

    # os.system('rm data.json')
    params = {'api_key': 'DEMO_KEY'} 
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    img, data = getAPOD(params)
    setWallpaper(img)
    
