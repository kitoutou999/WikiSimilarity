# -*- coding: utf-8 -*-
import json
import os

class SimilarityCalculator:
    def __init__(self, json_folder):
        self.json_folder = json_folder
        self.cp=0
        
        self.similarities = self.init_similarities()

    def bool_similarity(self, gold: int) -> dict:
                
        sorted_similarities = sorted(self.similarities.items(), key=lambda item: item[1], reverse=True)

        result = {}

        for i, (pair, sim) in enumerate(sorted_similarities):
            result[pair] = i < gold

        return result
    
    def init_similarities(self):
        file_path = os.path.join(os.path.dirname(__file__), self.json_folder)
        with open(file_path, 'r') as file:
            data = json.load(file)

        
        similarities = {}
        for key, value in data.items():
            key_tuple = tuple(key.strip("()").replace("'","").split(", "))
            similarities[key_tuple] = value

            
        return similarities
    
    def getSimilarities(self):
        return self.similarities

if __name__ == "__main__":
    calc = SimilarityCalculator('pre_calcule_similaritiesV2.json')
    
    #print(calc.getSimilarities())
    gold = int(len(calc.getSimilarities())*13.49//100)
    results = calc.bool_similarity(gold)
    
    print("Chargement de la donnée en cours (~1sec) . . .")
    #ANSI
    GREEN = "\033[32m"  
    RED = "\033[31m"    
    RESET = "\033[0m"  
    BOLD = "\033[1m"

    for key, values in results.items():
        similarity_status = f"{GREEN}similaires{RESET}" if values else f"{RED}peu similaires{RESET}"
        print(f"{key[0]} et {key[1]} sont {similarity_status}")
        
        
    print(f"\n{BOLD}Les {gold}(13.49%) premiers sont similaires{RESET}")
