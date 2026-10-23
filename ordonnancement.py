
from bellman import bellman, bellman_inverse
from contraintes import SIGMA

# Toutes les fonctions acceptent un paramètre facultatif arcs_sup : la liste des arcs (i, j, q)
# des contraintes supplémentaires (voir contraintes.py). Sans lui, seules les précédences comptent.

TAU = -1  # tâche fictive de fin de projet (durée 0), utilisée pour les dates au plus tard


def arcs_graphe(taches, arcs_sup=None):
    # Construction des arcs à partir des précédences
    arcs = [
        (i, j, taches[i]["duree"])
        for j, t in taches.items()
        for i in t["precedente"]
    ]
    # Aucune tâche ne commence avant le début du projet : Si >= So + 0 (cours p.11)
    arcs += [(SIGMA, i, 0) for i in taches]

    return arcs + list(arcs_sup or [])


def datesAuPlusTot(taches, arcs_sup=None):
    # Plus longs chemins depuis So (Bellman, cours p.11)
    s = {i: 0 for i in taches}
    s[SIGMA] = 0
    n = len(s)

    s = bellman_inverse(arcs_graphe(taches, arcs_sup), s, n)

    # So doit rester à 0 : sinon une contrainte impose de commencer avant le début du projet
    if s[SIGMA] != 0:
        raise ValueError("Dépendances circulaires")

    del s[SIGMA]
    return s

def dureeProjet(taches, arcs_sup=None):
    s = datesAuPlusTot(taches, arcs_sup)

    return max(
        s[i] + taches[i]["duree"]
        for i in taches
    )


def datesAuPlusTard(taches, arcs_sup=None):
    # Plus courts chemins depuis la fin du projet dans le graphe inverse
    # (arcs et poids opposés), en supposant S_fin = durée du projet (cours p.16)
    duree = dureeProjet(taches, arcs_sup)

    # On ajoute la fin fictive : chaque tâche doit être finie avant elle (Sfin >= Si + di)
    arcs = arcs_graphe(taches, arcs_sup) + [(i, TAU, taches[i]["duree"]) for i in taches]

    #construction arcs inverse
    arcs_inverses = [(j, i, -q) for i, j, q in arcs]

    dates = {i: float("inf") for i in taches}
    dates[TAU] = duree
    dates[SIGMA] = 0  # le début du projet reste fixé à 0

    dates = bellman(arcs_inverses, dates, len(dates))

    return {i: dates[i] for i in taches}




def datesTacheX(x,taches,fonctionDate):
    if x not in taches:
        raise ValueError(f"La tâche {x} n'existe pas")

    return fonctionDate(taches)[x]


def margesTaches(taches, arcs_sup=None):
    dateTot = datesAuPlusTot(taches, arcs_sup)
    dateTard = datesAuPlusTard(taches, arcs_sup)

    marges = {}

    for i in taches:
        marges[i]=dateTard[i] - dateTot[i]

    return marges

def tachesCritique(margesTaches):

    taches = []
    for i in margesTaches :
        if margesTaches[i]==0 :
            taches.append(i)
    return taches
