import json
import os

films = json.load(open('../../data/films.json', 'r', encoding='utf8'))

cinemas = json.load(open('../../data/cinemas.json', 'r', encoding='utf8'))
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
        
        current_film['numberEntries'] += film['numberEntries']
        current_film["recipe"] += film['recipe']
        if cinema['_id'] not in current_film['cinemas']:
            current_film['cinemas'].append(cinema['_id'])


json.dump(films, open('../../data/films.json', 'w', encoding='utf8'), indent=4, ensure_ascii=False)