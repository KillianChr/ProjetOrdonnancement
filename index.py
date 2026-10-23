
import json

from read import read, inverser
from graphValide import verifier_graphe
from ordonnancement import (
    dureeProjet,
    datesAuPlusTard,
    datesAuPlusTot,
    margesTaches,
    tachesCritique
)

nb_task, graphe = read()
graphe_inverse = inverser(graphe, nb_task)

if verifier_graphe(graphe):
    # initialisation
    duree = dureeProjet(graphe)
    dates_tot = datesAuPlusTot(graphe)
    dates_tard = datesAuPlusTard(graphe)
    marges = margesTaches(graphe)
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

# json
with open("resultat.json", "w", encoding="utf-8") as fichier:
    json.dump(resultat, fichier, ensure_ascii=False, indent=4)