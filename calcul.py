"""
Point d'entrée des calculs pour l'interface web (Symfony).

Utilisation :
    python calcul.py < projet.json

- Entrée (stdin)  : le projet en JSON, envoyé par web/src/Service/CalculOrdonnancement.php
    {
      "nom": "Construction maison",
      "taches": [ {"id": 1, "description": "Murs", "duree": 7, "precedentes": []}, ... ],
      "contraintes": [ {"type": "date_fixe", "tacheA": 2, "tacheB": null, "valeur": 3}, ... ]
        (types possibles : voir contraintes.TYPES)
    }
- Sortie (stdout) : le résultat en JSON, au même format que resultat.json produit par index.py,
  avec en plus un champ "erreur" (null si tout va bien).

Le script ne plante jamais : toute erreur est renvoyée dans le champ "erreur".
"""

import contextlib
import io
import json
import sys

from contraintes import contraintes
from graphValide import verifier_graphe
from ordonnancement import (
    dureeProjet,
    datesAuPlusTard,
    datesAuPlusTot,
    margesTaches,
    tachesCritique,
)


def construire_graphe(projet):
    """Transforme les tâches reçues en JSON au format utilisé par le reste du code (comme read())."""
    return {
        int(t["id"]): {
            "description": t["description"],
            "duree": int(t["duree"]),
            "precedente": [int(p) for p in t.get("precedentes", [])],
        }
        for t in projet.get("taches", [])
    }


def calculer(graphe, arcs_sup=None):
    """
    Calcule durée, dates, marges et tâches critiques (structure du resultat.json de index.py).
    arcs_sup : arcs des contraintes supplémentaires (voir contraintes.py), facultatif.
    """
    duree = dureeProjet(graphe, arcs_sup)
    dates_tot = datesAuPlusTot(graphe, arcs_sup)
    dates_tard = datesAuPlusTard(graphe, arcs_sup)
    marges = margesTaches(graphe, arcs_sup)
    critiques = tachesCritique(marges)

    taches = {}
    for identifiant, tache in graphe.items():
        taches[identifiant] = {
            "description": tache["description"],
            "duree": tache["duree"],
            "precedentes": tache["precedente"],
            "date_au_plus_tot": dates_tot[identifiant],
            "date_au_plus_tard": dates_tard[identifiant],
            "marge": marges[identifiant],
            "critique": identifiant in critiques,
        }

    return {"realisable": True, "duree_projet": duree, "taches": taches, "erreur": None}


def echec(message):
    """Résultat renvoyé quand le projet n'est pas réalisable ou que les données sont invalides."""
    return {"realisable": False, "duree_projet": None, "taches": {}, "erreur": message}


def main():
    # Les fonctions existantes peuvent faire des print() (ex. verifier_graphe en cas de cycle) :
    # on les capture pour qu'ils ne se mélangent pas au JSON, et on s'en sert comme message d'erreur.
    sortie_parasite = io.StringIO()

    try:
        projet = json.load(sys.stdin)
        graphe = construire_graphe(projet)
        liste_contraintes = projet.get("contraintes") or []

        if not graphe:
            resultat = echec("Le projet ne contient aucune tâche.")
        else:
            with contextlib.redirect_stdout(sortie_parasite):
                valide = verifier_graphe(graphe)
                if valide:
                    # Les contraintes deviennent des arcs ajoutés au graphe (lève ValueError si mal formées)
                    arcs_sup = contraintes(graphe, liste_contraintes)
                    try:
                        resultat = calculer(graphe, arcs_sup)
                    except ValueError:
                        # Bellman a trouvé un circuit de longueur positive : contraintes incompatibles
                        resultat = echec("Projet non réalisable : les contraintes sont incompatibles entre elles "
                                         "(circuit de longueur positive dans le graphe).")
                else:
                    resultat = None

            if resultat is None:
                detail = sortie_parasite.getvalue().strip()
                resultat = echec(detail or "Graphe invalide : vérifiez les précédentes, "
                                           "les durées et qu'au moins une tâche n'a pas de précédente.")

    except json.JSONDecodeError:
        resultat = echec("Données reçues illisibles (JSON invalide).")
    except (KeyError, TypeError, ValueError) as e:
        # ValueError : notamment une contrainte mal formée (tâche inexistante, type inconnu…)
        resultat = echec(f"Erreur : {e}")

    print(json.dumps(resultat, ensure_ascii=False))


if __name__ == "__main__":
    main()
