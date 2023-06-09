import faker
import json
import os
import bson

fake = faker.Faker('fr_FR')

films = []

categories = json.load(open('../../data/categories.json', 'r', encoding='utf8'))
nb_categories = len(categories)

producers = json.load(open('../../data/producers.json', 'r', encoding='utf8'))
nb_producers = len(producers)

actors = json.load(open('../../data/actors.json', 'r', encoding='utf8'))
nb_actors = len(actors)

for i in range(500):
    # film general infos
    film = {
        '_id': str(bson.ObjectId()),
        'title': fake.unique.sentence(nb_words=3)[0:-1],
        'synopsis': fake.text(),
        'releaseDate': fake.date_between(start_date='-30y', end_date='now').strftime('%Y-%m-%d'),
        'duration': fake.random_int(min=60, max=120),
        'numberEntries': 0,
        'recipe': 0,
        'cinemas': [],
    }

    # categories
    random_number_category = fake.random_int(min=1, max=5)
    film["categories"] = []
    for i in range(random_number_category):
        random_index = fake.random_int(min=0, max=nb_categories-1)
        category = categories[random_index]
        if category["name"] not in film["categories"]:
            film["categories"].append(category["name"])


    # actors
    random_number_actor = fake.random_int(min=5, max=10)
    film["actors"] = []
    for i in range(random_number_actor):
        random_index = fake.random_int(min=0, max=nb_actors-1)
        actor = actors[random_index]
        if actor not in film["actors"]:
            film["actors"].append(actor)


    # producers
    have_multiple_producers = fake.boolean(chance_of_getting_true=10)
    random_producer_index = fake.random_int(min=0, max=nb_producers-1)
    film['producers'] = [producers[random_producer_index]]

    if have_multiple_producers:
        random_producer_index_two = fake.random_int(min=0, max=nb_producers-1)
        if random_producer_index_two != random_producer_index:
            film['producers'].append(producers[random_producer_index_two])
        else : 
            random_index = fake.random_int(min=0, max=nb_producers-1)
            film['producers'].append(producers[random_index])


    # feedbacks
    random_feedback = fake.random_int(min=0, max=10)
    feedbacks = []
    for i in range(random_feedback):
        feedback = {
            'comment': fake.text(max_nb_chars=200),
            'rating': fake.random_int(min=0, max=5),
        }
        feedbacks.append(feedback)

    film['feedbacks'] = feedbacks

    films.append(film)

# create json file with films
filename = os.path.join(os.path.dirname(__file__), '../../data', 'films.json')
with open(filename, 'w', encoding='utf8') as outfile:
    json.dump(films, outfile, indent=4, ensure_ascii=False)
