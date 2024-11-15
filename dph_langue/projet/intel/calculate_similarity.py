# -*- coding: utf-8 -*-
import os
import json
from itertools import combinations
from concurrent.futures import ThreadPoolExecutor, as_completed
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

class SimilarityCalculator:
    def __init__(self, json_folder, input_folder):
        self.json_folder = json_folder
        self.input_folder = input_folder

    def read_file_content(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def calculate_similarity(self, text1, text2):
        if not text1 or not text2:
            return 0.0
        vectorisation = TfidfVectorizer().fit_transform([text1, text2])
        vecteur = vectorisation.toarray()
        return cosine_similarity(vecteur)[0, 1]

    def calculate_similarity_for_pair(self, title1, title2):
        content1 = self.read_file_content(os.path.join(self.input_folder, f"{title1[:-5]}.txt"))
        content2 = self.read_file_content(os.path.join(self.input_folder, f"{title2[:-5]}.txt"))

        if content1 and content2:
            similarity = self.calculate_similarity(content1, content2)
            return (title1, title2), similarity
        else:
            print("erreur")
            return (title1, title2), None

    def calculate_all_similarities(self):
        json_files = [f for f in os.listdir(self.json_folder) if f.endswith('.json')]
        resultat = {}

        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(self.calculate_similarity_for_pair, title1, title2): (title1, title2)
                       for title1, title2 in combinations(json_files, 2)}

            for future in tqdm(as_completed(futures), total=len(futures), desc="Calculating similarities"):
                pair, similarity = future.result()
                if similarity is not None:
                    resultat[(pair[0][:-5],pair[1][:-5])] = similarity

        return resultat

    def save_similarities(self, similarities):
        similarities_str_keys = {str(key): value for key, value in similarities.items()}

        with open('intel/pre_calcule_similaritiesV1.json', 'w') as file:
            json.dump(similarities_str_keys, file)
            
    def bool_similarity(self, similarity: dict, gold: int) -> dict:
        sorted_similarities = sorted(similarity.items(), key=lambda item: item[1], reverse=True)
        
        result = {}
        
        for i, (pair, sim) in enumerate(sorted_similarities):
            
            result[pair] = i < gold
        
        return result
    
        
          
        
       
       
    
if __name__ == "__main__":
    GREEN = "\033[32m"  
    RED = "\033[31m"    
    RESET = "\033[0m"  
    BOLD = "\033[1m"
    
    print(f"{BOLD}Chargement de la donnée en cours (~5min) . . .{RESET}")

  
    
    calc = SimilarityCalculator("peopleJson2", "wikipedia_texts")
    similarities = calc.calculate_all_similarities()
    simi = calc.bool_similarity(similarities, len(similarities)*13//100)
    calc.save_similarities(simi)
