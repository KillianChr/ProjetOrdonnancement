
import json
import sys

from read import read, inverser
from contraintes import contraintes
from graphValide import verifier_graphe
from calcul import calculer

chemin = f"Graphe/{sys.argv[1] if len(sys.argv) > 1 else 'P1'}.csv"  # python index.py P2
nb_task, graphe = read(chemin)

try:
    extra = contraintes(chemin, graphe)  # contraintes propres au projet (voir contraintes.py)
    if verifier_graphe(graphe):
        # inverser() a besoin d'un graphe valide : il plante sur une précédente inexistante
        graphe_inverse = inverser(graphe, nb_task)
        # Les calculs et la structure du résultat sont dans calcul.py (partagés avec le site)
        resultat = calculer(graphe, extra)
    else:
        resultat = {
            "realisable": False,
            "erreur": "Graphe invalide"
        }
except ValueError as e:  # contraintes incompatibles, tâche inexistante ou dépendances circulaires
    resultat = {
        "realisable": False,
        "erreur": str(e)
    }

# json
with open("resultat.json", "w", encoding="utf-8") as fichier:
    json.dump(resultat, fichier, ensure_ascii=False, indent=4)
