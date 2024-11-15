# -*- coding: utf-8 -*-
import os
import wikipediaapi

class WikipediaExtractor:
    def __init__(self,input_folder ,output_folder):
        self.output_folder = output_folder
        self.json_folder = input_folder
        
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

    def get_wikipedia_page_content(self,title):
        user_agent = 'anonym/1.0 (https://anonym.com; anonym@gmail.com)'
        wiki_wiki = wikipediaapi.Wikipedia(user_agent,'en')
        
        page = wiki_wiki.page(title)
        if page.exists():
            return page.text
        else:
            return None

    def save_content_to_file(self, title, content):
        file_path = os.path.join(self.output_folder, f"{title}.txt")
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

    def extract_and_save(self):
        json_files = [f for f in os.listdir(self.json_folder) if f.endswith('.json')]
        cp = 0
        for elt in json_files:
            
            title = elt[:-5]
            content = self.get_wikipedia_page_content(title)
            if content:
                cp+=1
                self.save_content_to_file(title, content)
                print(f"Saved content for {title}. [{cp}/{len(json_files)}]")
                

if __name__ == "__main__":
    output_folder = "wikipedia_texts"
    input_folder = "peopleJson2"
    extractor = WikipediaExtractor( input_folder,output_folder)
    extractor.extract_and_save()