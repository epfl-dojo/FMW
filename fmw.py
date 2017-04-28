#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
# FBI API - https://api.fbi.gov/docs/wanted/index.html
html_page = requests.get('https://www.fbi.gov/wanted/cyber')
#html_page = requests.get("https://api.fbi.gov/wanted/v1")
html_txt = html_page.text
soup = BeautifulSoup(html_txt, 'html.parser')
names = soup.findAll("div", { "class" : "focuspoint" })
# print(names[0].attrs['data-base-url'])
for criminal in names :
    url_personne = criminal.attrs['data-base-url'].split('@@')[0]
    name = criminal.img.attrs['alt']
    print(name + " : " + url_personne)

#url_personne = names[0].attrs['data-base-url']
#print(url_personne.split('@@')[0])
