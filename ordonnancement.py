
from bellman import bellman, bellman_inverse
from contraintes import SIGMA

FIN = "fin"  # sommet fictif de fin de projet
# extra = arcs (i, j, q) supplémentaires (Sj >= Si + q), par ex. contraintes(taches)

def arcsPrecedences(taches):
    # Construction des arcs à partir des précédences
    return [
        (i, j, taches[i]["duree"])
        for j, t in taches.items()
        for i in t["precedente"]
    ]

def datesAuPlusTot(taches, extra=()):
    arcs = arcsPrecedences(taches) + list(extra)

    s = {i: 0 for i in taches}
    s[SIGMA] = 0  # début du projet
    n = len(taches) + 1  # sommets : les tâches + SIGMA

    s = bellman_inverse(arcs, s, n)
    return {i: s[i] for i in taches}

def dureeProjet(taches, extra=()):
    s = datesAuPlusTot(taches, extra)

    return max(
        s[i] + taches[i]["duree"]
        for i in taches
    )


def datesAuPlusTard(taches, extra=()):
    duree = dureeProjet(taches, extra)

    # tous les arcs, plus un arc i -> FIN de poids durée(i) : FIN >= Si + durée(i)
    arcs = arcsPrecedences(taches) + list(extra) + [(i, FIN, taches[i]["duree"]) for i in taches]
    # arcs inversés : Si <= Sj - q
    arcs = [(j, i, -q) for i, j, q in arcs]

    dates = {i: float("inf") for i in taches}
    dates[SIGMA] = 0
    dates[FIN] = duree
    n = len(taches) + 2  # sommets : les tâches + SIGMA + FIN

    dates = bellman(arcs, dates, n)
    return {i: dates[i] for i in taches}


def datesTacheX(x,taches,fonctionDate,extra=()):
    if x not in taches:
        raise ValueError(f"La tâche {x} n'existe pas")

    return fonctionDate(taches, extra)[x]


def margesTaches(taches, extra=()):
    dateTot = datesAuPlusTot(taches, extra)
    dateTard = datesAuPlusTard(taches, extra)

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

        