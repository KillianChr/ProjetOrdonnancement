"""
Point d'entrée des calculs pour l'interface web (Symfony).

Utilisation :
    python calcul.py < projet.json

- Entrée (stdin)  : le projet en JSON, envoyé par web/src/Service/CalculOrdonnancement.php
    {
      "nom": "Construction maison",
      "taches": [ {"id": 1, "description": "Murs", "duree": 7, "precedentes": []}, ... ],
      "contraintes": [ {"type": "date_fixe", "tacheA": 2, "tacheB": null, "valeur": 3}, ... ]
        (types : les fonctions de contraintes.py, plus "debut_max_apres_fin" traduit ci-dessous)
    }
- Sortie (stdout) : le résultat en JSON, au même format que resultat.json produit par index.py,
  avec en plus un champ "erreur" (null si tout va bien).

Le script ne plante jamais : toute erreur est renvoyée dans le champ "erreur".
"""

import contextlib
import io
import json
import sys

from contraintes import SIGMA, arcs_contrainte
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


def traduire_contrainte(contrainte, graphe):
    """Traduit une contrainte du site (type, tacheA, tacheB, valeur) en appel de contraintes.py : (nom, paramètres)."""
    nom = contrainte.get("type")
    a = contrainte.get("tacheA")
    b = contrainte.get("tacheB")
    x = int(contrainte.get("valeur") or 0)

    if nom in ("date_fixe", "date_min", "date_max"):
        return nom, [a, x]
    if nom == "apres_debut":
        return nom, [a, b, x]
    if nom == "debut_max_apres_fin":
        # Cours p.20 : Sb <= Sa + da + x  <=>  Sa >= Sb - da - x, soit apres_debut(b, a, -(da + x))
        return "apres_debut", [b, a, -(graphe[a]["duree"] + x)]
    return nom, [a, b]  # precedence, chevauchement (un type inconnu est refusé par arcs_contrainte)


def arcs_contraintes(liste, graphe):
    """Arcs des contraintes du site, comme contraintes() de contraintes.py le fait pour un fichier."""
    arcs = [(SIGMA, i, 0) for i in graphe]  # aucune tâche ne commence avant le début du projet
    for contrainte in liste:
        nom, params = traduire_contrainte(contrainte, graphe)
        arcs += arcs_contrainte(nom, params, graphe)
    return arcs


def calculer(graphe, extra=()):
    """
    Calcule durée, dates, marges et tâches critiques (structure du resultat.json de index.py).
    extra : arcs des contraintes supplémentaires, facultatif.
    """
    duree = dureeProjet(graphe, extra)
    dates_tot = datesAuPlusTot(graphe, extra)
    dates_tard = datesAuPlusTard(graphe, extra)
    marges = margesTaches(graphe, extra)
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
                    extra = arcs_contraintes(liste_contraintes, graphe)
                    try:
                        resultat = calculer(graphe, extra)
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
