import faker
import json
import os

fake = faker.Faker('fr_FR')

cinemas = []

for i in range(50):
    cinema = {
        'name': fake.company(),
        'city': fake.city(),
    }

    cinemas.append(cinema)

# create json file with films
filename = os.path.join(os.path.dirname(__file__), '..', 'cinemas.json')
with open(filename, 'w', encoding='utf8') as outfile:
    json.dump(cinemas, outfile, indent=4, ensure_ascii=False)
