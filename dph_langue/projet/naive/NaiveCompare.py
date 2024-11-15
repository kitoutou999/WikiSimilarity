# -*- coding: utf-8 -*-
import os
from collections import defaultdict

class NaiveCompare:
    
    def __init__(self, dossier, pourcentage_similaire=100):
        self.dossier = dossier
        self.resultats = defaultdict(float)
        self.pourcentage_similaire = pourcentage_similaire

    def comparer_fichiers(self):
        fichiers = [f for f in os.listdir(self.dossier) if f.endswith('.txt')]
        
        for i, fichier1 in enumerate(fichiers):
            with open(os.path.join(self.dossier, fichier1), 'r', encoding='utf-8', errors='ignore') as f1:
                liens1 = set(f1.read().splitlines())
            
            for fichier2 in fichiers[i+1:]:
                with open(os.path.join(self.dossier, fichier2), 'r', encoding='utf-8', errors='ignore') as f2:
                    liens2 = set(f2.read().splitlines())
                
                liens_communs = liens1.intersection(liens2)
                total_liens_uniques = liens1.union(liens2)
                
                if total_liens_uniques:
                    similarite = len(liens_communs) / len(total_liens_uniques)
                else:
                    similarite = 0
                
                self.resultats[(fichier1[:-4], fichier2[:-4])] = similarite

    def obtenir_resultats_tries(self):
        return sorted(self.resultats.items(), key=lambda x: x[1], reverse=True)

    def afficher_resultats(self):
        GREEN = "\033[32m"   # Vert
        RED = "\033[31m"     # Rouge
        BOLD = "\033[1m"     # Gras
        RESET = "\033[0m"    # Réinitialiser le style
        resultats_finaux = self.get_resultats()
        for (fichier1, fichier2), est_similaire in resultats_finaux.items():
            status = f"{BOLD}{GREEN}similaires{RESET}" if est_similaire else f"{BOLD}{RED}peu similaires{RESET}"
            print(f"{fichier1}, {fichier2}: {status}")

    def get_resultats(self):
        resultats_tries = self.obtenir_resultats_tries()
        nombre_resultats = len(resultats_tries)
        nombre_a_garder = int(nombre_resultats * (self.pourcentage_similaire/100))
        resultats_finaux = {}
        for i, ((fichier1, fichier2), _) in enumerate(resultats_tries):
            if i >= nombre_a_garder:
                resultats_finaux[(fichier1, fichier2)] = False
            else:
                resultats_finaux[(fichier1, fichier2)] = True
        return resultats_finaux
    
    @staticmethod
    def calculer_pourcentage_true(resultats):
        total = len(resultats)
        true_count = sum(1 for isGold in resultats.values() if isGold)
        return (true_count / total) * 100 if total > 0 else 0

if __name__ == "__main__":
    
    dossier_naivecompare = 'peopleLink'

    parametre = int(input("Veuillez entrer le seuil (x premier %)(exemple: 10): "))
    print("Chargement de la donnée en cours (~10s) . . .")
    comparateur = NaiveCompare(dossier_naivecompare, parametre)
    comparateur.comparer_fichiers()
    comparateur.afficher_resultats()

