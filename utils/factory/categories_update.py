import json
import os

categories = json.load(open('../categories.json', 'r', encoding='utf8'))

films = json.load(open('../films.json', 'r', encoding='utf8'))
nb_films = len(films)

for i in range(nb_films-1):
    film_categories = films[i]['categories']
    for j in range(len(film_categories)):
        name = film_categories[j]

        current_category = next(
            (f for f in categories if f["name"] == name), None)

        film = {"film": films[i]['_id'],
                "title": films[i]['title'],
                "numberEntries": films[i]['numberEntries'],
                "recipe": films[i]['recipe']
                }
        current_category['films'].append(film)

# create json file with categories
filename = os.path.join(os.path.dirname(__file__), '..', 'categories.json')
with open(filename, 'w', encoding='utf8') as outfile:
    json.dump(categories, outfile, indent=4, ensure_ascii=False)
