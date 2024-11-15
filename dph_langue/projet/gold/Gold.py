# -*- coding: utf-8 -*-
import os
import json
from itertools import combinations


class Gold: 

    def __init__(self, json_folder):
        self.json_folder = json_folder
        self.similarity_scores = []
        self.threshold = None

    def load_json(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def compare_jsons(self, json1, json2):
        common_categories = set(json1.keys()) & set(json2.keys())
        total_categories = len(set(json1.keys()) | set(json2.keys()))
        
        if not common_categories:
            return 0

        category_scores = []
        for key in common_categories:
            category_scores.append(0.5)
            if isinstance(json1[key], list) and isinstance(json2[key], list):
                common_elements = set(json1[key]) & set(json2[key])
                total_elements = len(set(json1[key]) | set(json2[key]))
                category_scores.append(len(common_elements) / total_elements if total_elements > 0 else 0)
            elif json1[key] == json2[key]:
                category_scores.append(1)
            else:
                category_scores.append(0)

        average_category_score = sum(category_scores) / len(category_scores) if category_scores else 0
        proportion_common_categories = len(common_categories) / total_categories

        similarity_score = (average_category_score + proportion_common_categories) / 2
        return similarity_score

    def process_json_files(self):
        json_files = [f for f in os.listdir(self.json_folder) if f.endswith('.json')]
        
        results = {}
        
        for file1, file2 in combinations(json_files, 2):
            json1 = self.load_json(os.path.join(self.json_folder, file1))
            json2 = self.load_json(os.path.join(self.json_folder, file2))
            score = self.compare_jsons(json1, json2)
            self.similarity_scores.append(score)
            results[(file1, file2)] = score
        
        return results

    def calculate_threshold(self):
        if not self.similarity_scores:
            return 0

        # Calcul de la moyenne
        mean = sum(self.similarity_scores) / len(self.similarity_scores)

        # Calcul de l'écart-type
        variance = sum((x - mean) ** 2 for x in self.similarity_scores) / len(self.similarity_scores)
        std_dev = variance ** 0.5

        # Calcul du seuil (moyenne + écart-type)
        threshold = mean+std_dev

        return min(max(threshold, 0), 1)  # Assure que le seuil est entre 0 et 1

    def get_results(self):
        results = self.process_json_files()
        self.threshold = self.calculate_threshold()
        
        final_results = {}
        for (file1, file2), score in results.items():
            is_similar = score >= self.threshold
            final_results[(file1[:-5], file2[:-5])] = is_similar
        
        return final_results

# Utilisation
if __name__ == "__main__":
    print("Chargement de la donnée en cours (~10s) . . .")
    g = Gold("peopleJson2")
    results = g.get_results()
    #ANSI
    GREEN = "\033[32m"  
    RED = "\033[31m"    
    RESET = "\033[0m"  
    BOLD = "\033[1m"

    for key, values in results.items():
        similarity_status = f"{GREEN}similaires{RESET}" if values else f"{RED}peu similaires{RESET}"
        print(f"{key[0]} et {key[1]} sont {similarity_status}")

    print(f"\nSeuil calculé : {BOLD}{g.threshold}{RESET}")
    
