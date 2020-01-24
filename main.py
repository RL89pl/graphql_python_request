from openpyxl import load_workbook
from openpyxl import Workbook
import json
import os
import re
import requests
import base64
def decode64(tekst, numerid):
    nazwa = "{}:{}".format(tekst, numerid)
    decode = base64.b64encode(nazwa.encode())
    tekst = str(decode)[2:-1]
    return tekst
def WqlData():
    LISTA_PLIKOW = os.listdir("C:\\DIR\\DIR\\DIR\\")

    liczba = 0

    for plik in LISTA_PLIKOW:
        adres = "C:\\DIR\\DIR\\DIR\\" + plik
        
        nazwaPliku = plik.split(".")
        print("Edytuję: " + plik)
        nazwa = nazwaPliku[0]
        with open(adres, 'r+', encoding = 'utf-8') as f:
            data = json.load(f)
        aktualny = data[nazwa]["aktualny"]
        if aktualny != "1":
            pass
        else:
            
            if "-" in nazwa:
                kod_glowny = nazwa.split("-")
                kod = kod_glowny[0]
                wariant = nazwa
            else:
                kod = nazwa
                wariant = nazwa

            nazwa_pl = data[nazwa]["nazwa_pl"]
            nazwa_pl = '"%s"'%nazwa_pl
            opis_pl = data[nazwa]["opis_pl"]
            opis_pl = '"%s"'%opis_pl
            cena = data[nazwa]["ceny"]["PLN"]
            kategoria = data[nazwa]["kategoria"]
            if "Biuro" in kategoria:
                numerid = 5
            elif "Brelok" in kategoria:
                numerid = 6
            elif "Do pisania" in kategoria:
                numerid = 2
            elif "Elektronika" in kategoria:
                numerid = 1
            elif "Jedzenie" in kategoria:
                numerid = 7
            elif "odblaski" in kategoria:
                numerid = 8
            elif "Sport" in kategoria:
                numerid = 4
            elif "Torby" in kategoria:
                numerid = 9
            kategoria = decode64("Category", numerid)
            kategoria = '"%s"'%kategoria
            query = """
            mutation {
            tokenCreate(email: "EMAIL", password: "PASS") {
                token
            }
            }"""
            response = requests.post('http://DOMAIN/graphql/', json={'query': query})
            response = response.json()['data']['tokenCreate']
            token = response['token']
            headers = {"Authorization": "JWT " + token}
            query = """mutation {
            productCreate(input: {description: %s, name: %s, productType: "UHJvZHVjdFR5cGU6Mw==", basePrice: %s, category: %s , isPublished: true}) {
                product {
                id
                }
            }
            }"""%(opis_pl,nazwa_pl, cena, kategoria)
            url = 'http://DOMAIN/graphql/'
            r = requests.post(url, json={'query': query}, headers=headers)
            json_data = json.loads(r.text)
            df_data = json_data
            print(r.text)
            liczba +=1


if __name__ == '__main__':

    WqlData()

