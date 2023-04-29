import faker
import json
import os
import datetime

def str_to_date(date):
    return datetime.datetime.strptime(date, "%Y-%m-%d")

fake = faker.Faker('fr_FR')

cinemas = []

films = json.load(open('../films.json', 'r', encoding='utf8'))

for i in range(50):
    # general cinema information
    cinema = {
        '_id': fake.unique.pystr(min_chars=10, max_chars=10),
        'name': fake.company(),
        'city': fake.city(),
        'films': []
    }

    random_number_films = fake.random_int(min=5, max=60)
    nb_films = len(films)
    for j in range(random_number_films):
        # film information
        random_index = fake.random_int(min=0, max=nb_films-1)
        random_film = films[random_index]

        film_entries = 0
        film_recipes = 0

        film_date_release = random_film['releaseDate']
        film_date_end = str_to_date(film_date_release) + datetime.timedelta(days=365)
        film_date_end_diffusion = fake.date_between(start_date=str_to_date(film_date_release), end_date=film_date_end).strftime('%Y-%m-%d')
        film_duration = random_film['duration']

        # show information
        random_nb_show = fake.random_int(min=5, max=25)
        shows = []
        for k in range(random_nb_show):
            date_show = fake.date_between(
                start_date=str_to_date(film_date_release), 
                end_date=str_to_date(film_date_end_diffusion)
            )

            start_show = fake.time(pattern="%H:%M", end_datetime=None)
            start_show_date = datetime.datetime.strptime(start_show, "%H:%M")

            
            end_show = start_show_date + datetime.timedelta(minutes=film_duration)

            nb_entries = fake.random_int(min=0, max=200)
            price = fake.random_int(min=5, max=15)
            recipe = nb_entries * price

            show = {
                'salle' : fake.random_int(min=1, max=10),
                'dateShow': date_show.strftime('%Y-%m-%d'),
                'startShow': start_show,
                'endShow': end_show.strftime('%H:%M'),
                'durationShow': film_duration,
                'numberEntries': nb_entries,
                'price': price,
                'recipe': recipe
            }
            film_entries += nb_entries
            film_recipes += recipe
            shows.append(show)

        film = {
            'film': films[random_index]['_id'],
            'title': films[random_index]['title'],
            'numberEntries': film_entries,
            'recipe' : film_recipes,
            'filmShow': shows,
            'startDiffusion': film_date_release,
            'endDiffusion': film_date_end_diffusion,
        }
        cinema['films'].append(film)

    cinemas.append(cinema)

# create json file with films
filename = os.path.join(os.path.dirname(__file__), '..', 'cinemas.json')
with open(filename, 'w', encoding='utf8') as outfile:
    json.dump(cinemas, outfile, indent=4, ensure_ascii=False)
