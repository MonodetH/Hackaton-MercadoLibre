import http.client, urllib, json, requests
from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup

# Create your views here.

def index(request):

    #get item
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '99fd5eb582914f7a8595822812988b94',
    }

    body = {"documents": [{"id": "1", "text": "pantalla mala, 16Gb de memoria"}]}

    conn = http.client.HTTPSConnection('api.mercadolibre.com')
    conn.request("GET", "/items/MLC443958984?access_token=APP_USR-3443485718526955-061017-d1f66ff2a267adde4dd51cf57dc7b817__A_K__-4452942", body="{}", headers=headers)
    response = conn.getresponse()
    item = response.read()
    conn.close()

    #description
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '99fd5eb582914f7a8595822812988b94',
    }

    body = {"documents": [{"id": "1", "text": "pantalla mala, 16Gb de memoria"}]}

    conn = http.client.HTTPSConnection('api.mercadolibre.com')
    conn.request("GET",
                 "/items/MLC443958984/description",
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
    data = response.read()
    print(data)
    conn.close()


    return HttpResponse(data)