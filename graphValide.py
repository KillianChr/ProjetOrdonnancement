import csv
from graphlib import CycleError

# Vérification de la validité du graph

try:
    #fonction()
except CycleError as e:
    print("Erreur : dépendances circulaires ->", e.args[1])