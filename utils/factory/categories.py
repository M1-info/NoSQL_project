import json
import faker
import os

categories_name = ["Horreur", "Action", "Comédie", "Drame", "Thriller", "Science-fiction", "Fantastique", "Aventure", "Animation", "Policier", "Documentaire", "Historique", "Guerre", "Biopic", "Musical", "Western", "Romance", "Famille", "Sport", "Emission", "Jeunesse", "Spectacle", "Autre"]
categories = []

fake = faker.Faker('fr_FR')

for name in categories_name:
    category = {    '_id': fake.unique.pystr(min_chars=10, max_chars=10),
                    'name': name, 
                    'films': []}
    categories.append(category)

# create json file with categories
filename = os.path.join(os.path.dirname(__file__), '..', 'categories.json')
with open(filename, 'w', encoding='utf8') as outfile:
    json.dump(categories, outfile, indent=4, ensure_ascii=False)