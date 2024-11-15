# -*- coding: utf-8 -*-
from intel.intelligente import SimilarityCalculator
from naive.NaiveCompare import *
from gold.Gold import *
from collections import defaultdict
import matplotlib.pyplot as plt
import sys
class Metriques:
    
    def __init__(self):
        self.analyse_metrique_naive={
            'VP':[],
            'FP':[],
            'VN': [],
            'FN':[],
        }
        self.analyse_metrique_intel={
            'VP':[],
            'FP':[],
            'VN': [],
            'FN':[],
        }

    def calculer_pourcentage_true(self,resultats):
        total = len(resultats)
        true_count = sum(1 for isGold in resultats.values() if isGold)
        return (true_count / total) * 100 if total > 0 else 0

    def calculer_metriques(self,predictions, references,naive):
        analyse_metrique = {
            'VP': [],
            'FP': [],
            'VN': [],
            'FN': []
            
        }
        vp = fp = vn = fn = 0
        for cle in set(predictions.keys()) | set(references.keys()):
            pred = predictions.get(cle)
            ref = references.get(cle)
            if pred and ref:
                vp += 1
                analyse_metrique['VP'].append(cle)
            elif pred and not ref:
                fp += 1
                analyse_metrique['FP'].append(cle)
            elif not pred and ref:
                fn += 1
                analyse_metrique['FN'].append(cle)
            else:
                vn += 1
                analyse_metrique['VN'].append(cle)
                
        if naive:
            self.analyse_metrique_naive = analyse_metrique
        else:
            self.analyse_metrique_intel = analyse_metrique
        

        print(f"{GREEN}VP {RESET}: {vp}")
        print(f"{RED}F{RESET}{GREEN}P{RESET}: {fp}")
        print(f"{RED}FN{RESET} : {fn}")    
        
        exactitude = (vp + vn) / (vp + vn + fp + fn) if (vp + vn + fp + fn) > 0 else 0
        precision = vp / (vp + fp) if (vp + fp) > 0 else 0
        rappel = vp / (vp + fn) if (vp + fn) > 0 else 0
        f_mesure = 2 * ((precision * rappel) / (precision + rappel)) if (precision + rappel) > 0 else 0
        
        return {
            'precision': precision,
            'rappel': rappel,
            'f_mesure': f_mesure
        }

    def calculer_metriques_macro(self,predictions, references):
        metriques_par_classe = defaultdict(lambda: {'vp': 0, 'fp': 0, 'fn': 0, 'vn': 0})
        
        for cle in set(predictions.keys()) | set(references.keys()):
            pred = predictions.get(cle, False)
            ref = references.get(cle, False)
            if pred and ref:
                metriques_par_classe[True]['vp'] += 1
                metriques_par_classe[False]['vn'] += 1
            elif pred and not ref:
                metriques_par_classe[True]['fp'] += 1
                metriques_par_classe[False]['vn'] += 1
            elif not pred and ref:
                metriques_par_classe[True]['fn'] += 1
                metriques_par_classe[False]['vn'] += 1
            else:
                metriques_par_classe[True]['vn'] += 1
                metriques_par_classe[False]['vp'] += 1
        
        macro_metriques = {
            'precision': 0,
            'rappel': 0,
            'f_mesure': 0
        }
        
        for classe, metriques in metriques_par_classe.items():
            precision = metriques['vp'] / (metriques['vp'] + metriques['fp']) if (metriques['vp'] + metriques['fp']) > 0 else 0
            rappel = metriques['vp'] / (metriques['vp'] + metriques['fn']) if (metriques['vp'] + metriques['fn']) > 0 else 0
            f_mesure = 2 * ((precision * rappel) / (precision + rappel)) if (precision + rappel) > 0 else 0
            
            macro_metriques['precision'] += precision
            macro_metriques['rappel'] += rappel
            macro_metriques['f_mesure'] += f_mesure
        
        for metrique in macro_metriques:
            macro_metriques[metrique] /= len(metriques_par_classe)
        
        return macro_metriques

    def calculer_metriques_micro(self,predictions, references):
        vp = fp = fn = vn = 0
        for cle in set(predictions.keys()) | set(references.keys()):
            pred = predictions.get(cle, False)
            ref = references.get(cle, False)
            if pred and ref:
                vp += 1
            elif pred and not ref:
                fp += 1
            elif not pred and ref:
                fn += 1
            else:
                vn += 1
        
        precision = vp / (vp + fp) if (vp + fp) > 0 else 0
        rappel = vp / (vp + fn) if (vp + fn) > 0 else 0
        f_mesure = 2 * ((precision * rappel) / (precision + rappel)) if (precision + rappel) > 0 else 0
        
        return {
            'precision': precision,
            'rappel': rappel,
            'f_mesure': f_mesure
        }
        
        

    def afficher_metriques(self,metriques, metriques_macro, metriques_micro):

        print(f"\n{BOLD}{UNDERLINE}Metriques globales:{RESET}")
        for metrique, valeur in metriques.items():
            print(f"{metrique.capitalize()}: {valeur:.4f} ({LOW}{valeur*100:.2f}%{RESET})")

        print(f"\n{BOLD}{UNDERLINE}Metriques macro:{RESET}")
        for metrique, valeur in metriques_macro.items():
            print(f"{metrique.capitalize()}: {valeur:.4f} ({LOW}{valeur*100:.2f}%{RESET})")

        """
        print(f"\n{BOLD}{UNDERLINE}Metriques micro:{RESET}")
        for metrique, valeur in metriques_micro.items():
            print(f"{metrique.capitalize()}: {valeur:.4f} ({LOW}{valeur*100:.2f}%{RESET})")
        """

    def save_analyse_Stats(self, analyse_metrique_naive, analyse_metrique_intel):
        categories = ['VP', 'FP', 'FN']
        pourcentages_naive = []
        pourcentages_intel = []

        print(f"\n\n{RED}WARNING : Ceci est le taux d'element de l'intersection dans chaque approche{RESET}")

        for key in categories:
            value_naive = analyse_metrique_naive[key]
            value_intel = analyse_metrique_intel[key]
            
            intersection = set(value_naive).intersection(set(value_intel))
            
            if not os.path.exists('intel/AnalyseStats'):
                os.makedirs('intel/AnalyseStats')

            # Sauvegarder les intersections dans des fichiers
            with open(f"intel/AnalyseStats/analyse_metrique_{key}.txt", "w") as file:
                for elt in intersection:
                    file.write(f"{elt}\n")

            # Calcul des pourcentages pour les affichages
            naive_pct = len(intersection) / len(value_naive) * 100 if len(value_naive) > 0 else 0
            intel_pct = len(intersection) / len(value_intel) * 100 if len(value_intel) > 0 else 0

            pourcentages_naive.append(naive_pct)
            pourcentages_intel.append(intel_pct)

            # Affichage des résultats en texte
            print("\n")
            print(f"{BOLD}{UNDERLINE}Analyse des {key} :{RESET}")
            print(f"{key} : {len(intersection)} soit {naive_pct:.2f}% de {key} de l'approche naive")
            print(f"{key} : {len(intersection)} soit {intel_pct:.2f}% de {key} de l'approche intel")
            print(f"Soit une difference de {abs(naive_pct - intel_pct):.2f}% entre les deux approches")


        
        if len(sys.argv) > 1:
            if sys.argv[1] == "-s":
                # Création du graphique
                x = range(len(categories))
                width = 0.35  # Largeur des barres

                plt.figure(figsize=(10, 6))
                plt.bar(x, pourcentages_naive, width, label='Naïve', color='skyblue')
                plt.bar([p + width for p in x], pourcentages_intel, width, label='Intel', color='salmon')

                # Ajout des labels et titre
                plt.xlabel("Métriques d'Evaluation")
                plt.ylabel("Taux d'éléments de l'intersection dans chaque approche (%)")
                plt.title("Comparaison des taux d'intersection entre l'approche naïve et l'approche intel")
                plt.xticks([p + width / 2 for p in x], categories)
                plt.legend()

                # Afficher le graphique
                plt.show()
                
            
        


if __name__ == "__main__":
    colorama = True
    if colorama:
        GREEN = "\033[32m"   # Vert
        RED = "\033[31m"     # Rouge
        BOLD = "\033[1m"     # Gras
        UNDERLINE = "\033[4m"#Souligner
        LOW = "\033[2m"#Basse intensité
        BLINK = "\033[5m"#Cligniote
        RESET = "\033[0m"    # Réinitialiser le style
    else:
        GREEN = ""   
        RED = ""     
        BOLD = ""    
        UNDERLINE = ""
        LOW = ""
        BLINK = ""
        RESET = ""   
    print(f"{BOLD}Chargement de la donnée en cours (~10s) {BLINK}. . .{RESET}")
    metri = Metriques()

    dossier_naivecompare = './peopleLink'
    dossier_gold = './peopleJson2'
    
    g = Gold(dossier_gold)
    resultats_gold = g.get_results()
  


    pourcentage_true_gold = metri.calculer_pourcentage_true(resultats_gold)
    

    comparateur_naive = NaiveCompare(dossier_naivecompare, pourcentage_true_gold)
    resultats_naive = comparateur_naive.comparer_fichiers()
    resultats_naive = comparateur_naive.get_resultats()
    
    resultat_intel = SimilarityCalculator('pre_calcule_similaritiesV2.json')
    gold = int(len(resultat_intel.getSimilarities())*(pourcentage_true_gold)//100) #renvoie le nombre de valeur que doit renvoyer l'approche intel avec le gold standar
    resultat_intel = resultat_intel.bool_similarity(gold)
    
    print(f"Pourcentage de couples similaires dans Gold: {pourcentage_true_gold:.2f}%\n")



    print(f"{BOLD}{UNDERLINE}Naïve x Gold Standard :{RESET}")
    metriques = metri.calculer_metriques(resultats_naive, resultats_gold,True)
    metriques_macro = metri.calculer_metriques_macro(resultats_naive, resultats_gold)
    metriques_micro = metri.calculer_metriques_micro(resultats_naive, resultats_gold)

    metri.afficher_metriques(metriques, metriques_macro, metriques_micro)
    print("\n\n")
        
        
    print(f"{BOLD}{UNDERLINE}Intelligent x Gold Standard :{RESET}")
    metriques = metri.calculer_metriques(resultat_intel, resultats_gold,False)
    
    metriques_macro = metri.calculer_metriques_macro(resultat_intel, resultats_gold)
    metriques_micro = metri.calculer_metriques_micro(resultat_intel, resultats_gold)

    metri.afficher_metriques(metriques, metriques_macro, metriques_micro)

    metri.save_analyse_Stats(metri.analyse_metrique_naive,metri.analyse_metrique_intel)

