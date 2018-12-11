from bs4 import BeautifulSoup
import requests
import time
import re


# Prende in input una stringa e la restituisce pulita da tutti i whitespace, tab ecc ecc.
# la stringa è il titolo dell articolo.
def cleanString(string):
    cleanedString = string.replace("\t","").replace("\n","").replace("\r","")
    return(cleanedString)

# Prende in input il titolo pulito dalla funzione di "sopra" e setta ogni singola parola
# in lower case cosi da poter essere riconosciuta all interno dell articolo. Tutto dentro un set.
def separateWordsFromTitle(cleanedTitle):
    words = set([word.lower() for word in re.findall(r'\b\w+\b',cleanedTitle)])
    return(words)

# Prende in input il titolo dell articolo e la lista delle mie parole interessanti, in questo caso article e facts;
def isAttrative(articleTitle, myFavouriteList):
	# cleanedTitle restituisce il titolo dell articolo pulito da tutti i whitespace, tab ecc ecc. 
    cleanedTitle = cleanString(articleTitle)
    # wordsInTitle restituisce le parole lower_case in un set.
    wordsInTitle = separateWordsFromTitle(cleanedTitle)
    # myFavouriteListLower, per ogni parola in myFavouriteList restituisce la parola lower_case.
    myFavouriteListLower = set([word.lower() for word in list(myFavouriteList)])
    # Crea un intersezione tra wordsInTitle e myFavouriteListLower
    result = list(wordsInTitle.intersection(set(myFavouriteListLower)))
    score = len(result) / len(myFavouriteListLower)
    return({"commonWords" : result, "score" : score})

url = "https://www.hdblog.it/"
# Parole che mi interessano, sostituire a proprio piacimento
facts = {"A2","Lite","PlayStation","PS","Update","Xiaomi A2 Lite","Bundle","Mi", "Amazon", "Alexa", "Echo Dot", "Dot", "Echo", "Telegram","Pie", "Kingdom Hearts"}
url_request = requests.get(url, timeout = 5)
soup = BeautifulSoup(url_request.content, 'html.parser')

count = 0
for article in soup.findAll("a", class_="title_new"):
    if count < 15:
        print("--------------------------- NEWS ---------------------------")
        attractiveness = isAttrative(article.text, facts)
        print("%.2f | %s | %s" % (attractiveness["score"], attractiveness["commonWords"], cleanString(article.text)))
        count = count + 1
        time.sleep(3)

