# -*- coding: utf-8 -*-
import os
import json
from itertools import combinations
from concurrent.futures import ThreadPoolExecutor, as_completed
from transformers import BertTokenizer, BertModel
import torch
from tqdm import tqdm

"""
Cette classe permet de calculer les similarités entre les textes des fichiers json en utilisant un modèle BERT pré-entraîné(IA).
"""
class BertCalculator:
    def __init__(self, json_folder, input_folder):
        self.json_folder = json_folder
        self.input_folder = input_folder
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertModel.from_pretrained('bert-base-uncased')
        
   

    def read_file_content(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def get_embeddings(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
        outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1)

    def calculate_similarity(self, text1, text2):
        if not text1 or not text2:
            return 0.0
        emb1 = self.get_embeddings(text1)
        emb2 = self.get_embeddings(text2)
        cosine_sim = torch.nn.functional.cosine_similarity(emb1, emb2)
        return cosine_sim.item()

    def calculate_similarity_for_pair(self, title1, title2):
        content1 = self.read_file_content(os.path.join(self.input_folder, f"{title1[:-5]}.txt"))
        content2 = self.read_file_content(os.path.join(self.input_folder, f"{title2[:-5]}.txt"))
  
        if content1 and content2:
            similarity = self.calculate_similarity(content1, content2)
            return (title1,title2), similarity
        else:
            print("erreur")
            return (title1,title2), None

    def calculate_all_similarities(self):
        json_files = [f for f in os.listdir(self.json_folder) if f.endswith('.json')]
        #json_files = json_files[:10] # pour faire des tests sans que se soit trop long(10 premiers fichiers)
        resultat = {}

        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(self.calculate_similarity_for_pair, title1, title2): (title1, title2)
                       for title1, title2 in combinations(json_files, 2)}

            for future in tqdm(as_completed(futures), total=len(futures), desc="Calculating similarities"):
                pair, similarity = future.result()
                if similarity is not None:
                    resultat[(pair[0][:-5], pair[1][:-5])] = similarity

        return resultat

    def save_similarities(self, similarities):
        similarities_str_keys = {str(key): value for key, value in similarities.items()}
        
        with open('intel/pre_calcule_similaritiesV2.json', 'w') as file:
            json.dump(similarities_str_keys, file)


if __name__ == "__main__":
    calc = BertCalculator("peopleJson2", "wikipedia_texts")
    similarities = calc.calculate_all_similarities()
    calc.save_similarities(similarities)
    
   