
import json
import sys

from read import read, inverser
from contraintes import contraintes
from graphValide import verifier_graphe
from ordonnancement import (
    dureeProjet,
    datesAuPlusTard,
    datesAuPlusTot,
    margesTaches,
    tachesCritique
)

chemin = f"Graphe/{sys.argv[1] if len(sys.argv) > 1 else 'P1'}.csv"  # python index.py P2
nb_task, graphe = read(chemin)
graphe_inverse = inverser(graphe, nb_task)

try:
    extra = contraintes(chemin, graphe)  # contraintes propres au projet (voir contraintes.py)
    if verifier_graphe(graphe):
        # initialisation
        duree = dureeProjet(graphe, extra)
        dates_tot = datesAuPlusTot(graphe, extra)
        dates_tard = datesAuPlusTard(graphe, extra)
        marges = margesTaches(graphe, extra)
        critiques = tachesCritique(marges)

        taches = {}

        for identifiant in graphe:
            tache = graphe[identifiant]

            taches[identifiant] = {
                "description": tache["description"],
                "duree": tache["duree"],
                "precedentes": tache["precedente"],
                "date_au_plus_tot": dates_tot[identifiant],
                "date_au_plus_tard": dates_tard[identifiant],
                "marge": marges[identifiant],
                "critique": identifiant in critiques
            }

        resultat = {
            "realisable": True,
            "duree_projet": duree,
            "taches": taches
        }

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