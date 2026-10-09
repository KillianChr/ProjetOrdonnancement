import csv
from graphlib import CycleError


try:
    #fonction()
except CycleError as e:
    print("Erreur : dépendances circulaires ->", e.args[1])