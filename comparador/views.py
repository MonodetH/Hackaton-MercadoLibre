import http.client, urllib, json, requests
from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
from django.template import RequestContext
from datetime import datetime

# Create your views here.

ITEMS_URLS = []

def index(request):
    data = {}
    data["items"] = []
    for itemURL in ITEMS_URLS:
        itemData = {}

        itemID = itemURL.split("-")
        itemID = itemID[0][-3:] + itemID[1]
        #get item
        headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': '99fd5eb582914f7a8595822812988b94',
        }

        conn = http.client.HTTPSConnection('api.mercadolibre.com')
        conn.request("GET", "/items/"+itemID+"?access_token=APP_USR-3443485718526955-061017-d1f66ff2a267adde4dd51cf57dc7b817__A_K__-4452942", body="{}", headers=headers)
        response = conn.getresponse()
        item = json.loads(response.read().decode("utf-8"))
        conn.close()

        itemData["itemURL"] = itemURL
        itemData["foto"] = item["pictures"][0]["url"]
        print(itemData["foto"])
        itemData["precio"] = item["price"]

        #description
        headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': '99fd5eb582914f7a8595822812988b94',
        }

        body = {"documents": [{"id": "1", "text": "pantalla mala, 16Gb de memoria"}]}

        conn = http.client.HTTPSConnection('api.mercadolibre.com')
        conn.request("GET",
                     "/items/"+itemID+"/description",
                     body="{}", headers=headers)
        response = conn.getresponse()
        desc = BeautifulSoup(json.loads(response.read().decode("utf-8"))["text"]).get_text()
        conn.close()

        print(desc)
        print(type(desc))


        # sentiment
        headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': '99fd5eb582914f7a8595822812988b94',
        }

        query = {"documents": [{"id": "1", "text": desc}]}

        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/text/analytics/v2.0/keyPhrases", body=json.dumps(query), headers=headers)
        response = conn.getresponse()
        keywords = response.read()
        print(data)
        conn.close()

    return HttpResponse(data)

def add(request):
    id = request.GET.get('id', '')
    if id != '':
        ITEMS_URLS.append(id)

    print(ITEMS_URLS)

    return index(request)