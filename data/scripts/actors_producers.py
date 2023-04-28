import json
import faker
import os

fake = faker.Faker('fr_FR')

persons = []
for i in range(100):
    person = {
        'firstName': fake.first_name(),
        'lastName': fake.last_name(),
    }
    persons.append(person)

filename = os.path.join(os.path.dirname(__file__), '..', 'actors.json')
with open(filename, 'w') as f:
    json.dump(persons, f, indent=4)