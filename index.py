
import json

from read import read
from graphValide import verifier_graphe
from calcul import calculer, echec

nb_task, graphe = read("Graphe/P1.csv")

# Les calculs et la structure du résultat sont dans calcul.py (partagés avec l'interface web)
if verifier_graphe(graphe):
    resultat = calculer(graphe)
else:
    resultat = echec("Graphe invalide")

# json
with open("resultat.json", "w", encoding="utf-8") as fichier:
    json.dump(resultat, fichier, ensure_ascii=False, indent=4)
