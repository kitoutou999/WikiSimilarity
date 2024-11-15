# 📊 Projet de Similarité sur Wikipédia

**Créateurs du projet :**  
Tom David, Florian Pépin, Emilien Huron

---

## 🎯 Exécution du Programme Principal

1. Ouvrir un terminal dans le dossier du projet.
2. Exécuter la commande : `python3 -u -X utf8 main.py`
   - **Optionnel** : pour afficher un graphique des (VP, FP, FN), utiliser la commande : `python3 -u -X utf8 main.py -s`
3. Attendre les résultats affichés dans le terminal.

---

## 🔍 Exécution des Programmes Secondaires

### Gold Standard

1. Ouvrir un terminal dans le dossier du projet.
2. Exécuter la commande : `python3 -u -X utf8 gold/Gold.py`
3. Attendre les résultats affichés dans le terminal.

### Approche Naïve

1. Ouvrir un terminal dans le dossier du projet.
2. Exécuter la commande : `python3 -u -X utf8 naive/NaiveCompare.py`
3. Attendre les résultats affichés dans le terminal.

### Approche Intelligente (Version Finale)

1. Ouvrir un terminal dans le dossier du projet.
2. Exécuter la commande : `python3 -u -X utf8 intel/intelligente.py`
3. Attendre les résultats affichés dans le terminal.

---

## 🗃️ Création des Corpus

### Extraction du Corpus Hyperliens (Wikipedia)

⚠️ **Librairie requise** : `bs4`

1. Ouvrir un terminal dans le dossier du projet.
2. Exécuter la commande : `python3 -u -X utf8 naive/extract_link.py`
3. Attendre les résultats affichés dans le terminal.

### Extraction du Corpus Texte (Wikipedia)

⚠️ **Librairie requise** : `wikipediaapi`

1. Ouvrir un terminal dans le dossier du projet.
2. Exécuter la commande : `python3 -u -X utf8 intel/extract_wikipedia.py`
3. Attendre les résultats affichés dans le terminal.

---

## 🧠 Différentes Parties de l'Approche Intelligente

### Version 1 de l’Approche Intelligente

⚠️ **Librairies requises** : `sklearn`, `scikit-learn`, `tqdm`  
⚠️ **Temps d'exécution minimum** : 10 minutes

1. Ouvrir un terminal dans le dossier du projet.
2. Exécuter la commande : `python3 -u -X utf8 intel/calculate_similarity.py`
3. Attendre les résultats affichés dans le terminal.

### Calculs avec BERT

⚠️ **Librairies requises** : `transformers`, `torch`, `tqdm`  
⚠️ **Temps d'exécution minimum** : 50 minutes (avec indicateur de progression)

1. Ouvrir un terminal dans le dossier du projet.
2. Exécuter la commande : `python3 -u -X utf8 intel/BertSearch.py`
3. Attendre les résultats affichés dans le terminal.

---

## ℹ️ Informations Supplémentaires

- **peopleJson2** : Corpus WikiData en format JSON
- **peopleLink** : Corpus Wikipedia en format Hyperliens
- **peopleText** : Corpus Wikipedia en format Texte
- **Calculs préenregistrés** :
  - Version BERT : `intel/pre_calcule_similaritiesV2.json`
  - Version intelligente V1 : `intel/pre_calcule_similaritiesV1.json`
- **Analyse des résultats** : Intersection des VP, FP, FN dans `intel/AnalyseStats`

---
