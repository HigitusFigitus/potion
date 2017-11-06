#import os.path
import yaml
from app import db, Potion

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# db_path = os.path.join(BASE_DIR, 'potions.db')

with open('fixtures/potions.yaml', 'r') as f:
    seed_data = yaml.load(f)

for sd in seed_data:
	current_seed = Potion(sd['potion_name'], sd['potion_type'], sd['potion_class'])
	db.session.add(current_seed)

db.session.commit()