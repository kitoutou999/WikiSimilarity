# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
import json

def extract_link(url):
    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.text, 'html.parser')
    
    liens = soup.find_all('a')
    liens_wikipedia = [f"https://en.wikipedia.org{lien['href']}" for lien in liens if lien.has_attr('href') and lien['href'].startswith('/wiki/')]
    
    return liens_wikipedia

chemin_dossier = 'peopleJson2'
chemin_sortie = 'peopleLink'
fichiers = os.listdir(chemin_dossier)

if not os.path.exists(chemin_sortie):
    os.makedirs(chemin_sortie)

for fichier in fichiers:
    chemin_fichier = os.path.join(chemin_dossier, fichier)
    with open(chemin_fichier, 'r', encoding='utf-8') as f:
        donnees = json.load(f)
    
    nom = donnees['nom']
    url_wikipedia = "https://en.wikipedia.org/wiki/" + nom
    
    liens = obtenir_liens_wikipedia(url_wikipedia)
    
    nom_fichier_sortie = fichier[:-5] + ".txt"
    chemin_fichier_sortie = os.path.join(chemin_sortie, nom_fichier_sortie)
    
    with open(chemin_fichier_sortie, 'w', encoding='utf-8') as f:
        for lien in liens:
            f.write(f"{lien}\n")
    
    print(f"Liens sauvegardés pour {nom} dans {nom_fichier_sortie}")

print("Traitement terminé")
