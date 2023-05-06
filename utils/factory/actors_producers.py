import json
import faker
import os

fake = faker.Faker('fr_FR')

actors = []
for i in range(100):
    person = {
        'firstName': fake.first_name(),
        'lastName': fake.last_name(),
    }
    actors.append(person)

# save in json file with persons in utf8
filename = os.path.join(os.path.dirname(__file__), '..', 'actors.json')
with open(filename, 'w', encoding='utf8') as outfile:
    json.dump(actors, outfile, indent=4, ensure_ascii=False)


producers = []
for i in range(100):
    person = {
        'firstName': fake.first_name(),
        'lastName': fake.last_name(),
    }
    producers.append(person)

# save in json file with persons in utf8
filename = os.path.join(os.path.dirname(__file__), '..', 'producers.json')
with open(filename, 'w', encoding='utf8') as outfile:
    json.dump(producers, outfile, indent=4, ensure_ascii=False)
