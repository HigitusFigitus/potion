import yaml
from app import db, Potion

with open('fixtures/potions.yaml', 'r') as f:
    seed_data = yaml.load(f)

for sd in seed_data:
    current_seed = Potion(sd['potion_name'],
                          sd['potion_type'],
                          sd['potion_class'])

    db.session.add(current_seed)

db.session.commit()
