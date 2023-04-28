import json
import os

films = json.load(open('../films.json', 'r', encoding='utf8'))

cinemas = json.load(open('../cinemas.json', 'r', encoding='utf8'))
nb_cinemas = len(cinemas)

for i in range(nb_cinemas-1):
    cinema = cinemas[i]
    films_diffused = cinema['films']

    for film in films_diffused:
        film_title = film['title']

        current_film = next((f for f in films if f["title"] == film_title), None)
        if current_film is None:
            print(film_title)
            continue
        
        current_film['nbEntries'] += film['nbEntries']
        current_film["recipe"] += film['recipe']


json.dump(films, open('../films.json', 'w', encoding='utf8'), indent=4, ensure_ascii=False)