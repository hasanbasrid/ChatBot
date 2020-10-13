import os
import random

curr = os.getcwd()
animals_file = open(os.path.join(curr, "name", "animals.txt"), "r")
adj_file = open(os.path.join(curr, "name", "adjectives.txt"), "r")

animals = animals_file.readlines()
adjectives = adj_file.readlines()

def create_random_name():
    animal = random.choice(animals).strip().lower()
    adjective = random.choice(adjectives).strip()
    
    return adjective + "-" + animal.split()[-1]
 
animals_file.close()
adj_file.close()