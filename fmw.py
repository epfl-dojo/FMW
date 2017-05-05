#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
# FBI API - https://api.fbi.gov/docs/wanted/index.html
html_page = requests.get('https://www.fbi.gov/wanted/cyber')
#html_page = requests.get("https://api.fbi.gov/wanted/v1")
html_txt = html_page.text
soup = BeautifulSoup(html_txt, 'html.parser')
names = soup.findAll("div", { "class" : "focuspoint" })

def getCriminal_name(criminal):
    return(name)

def getCriminal_detail(criminal):
    url_personne = criminal.attrs['data-base-url'].split('@@')[0]
    return(url_personne)

def getCriminals():
    return(names)

def getCriminalsList():
    criminals = {}
    for criminal in names :
        url_personne = criminal.attrs['data-base-url'].split('@@')[0]
        name = criminal.img.attrs['alt']
        criminals[name] = url_personne
    return criminals    


    #print(url_personne.split('@@')[0])
#url_personne = names[0].attrs['data-base-url']
if __name__ == '__main__':
    print(getCriminals())
