
from bellman import bellman, bellman_inverse

def datesAuPlusTot(taches):
    # Construction des arcs à partir des précédences
    arcs = [
        (i, j, taches[i]["duree"])
        for j, t in taches.items()
        for i in t["precedente"]
    ]

    s = {i: 0 for i in taches}
    n = len(taches)

    return bellman_inverse(arcs, s, n)

def dureeProjet(taches):
    s = datesAuPlusTot(taches)

    return max(
        s[i] + taches[i]["duree"]
        for i in taches
    )


def datesAuPlusTard(taches):
    #construction arcs inverse
    arcs = [
        (j, i, -taches[i]["duree"])
        for j, t in taches.items()
        for i in t["precedente"]
    ]
    dates = {i: float("inf") for i in taches}

    taches_precedentes = {
        j
        for i in taches
        for j in taches[i]["precedente"]
    }

    for i in taches:
        if i not in taches_precedentes:
            dates[i] = -taches[i]["duree"]

    distances = bellman(arcs, dates, len(taches))
    duree = dureeProjet(taches)

    return {
        i: duree + distances[i]
        for i in taches
    }




def datesTacheX(x,taches,fonctionDate):
    if x not in taches:
        raise ValueError(f"La tâche {x} n'existe pas")

    return fonctionDate(taches)[x]


def margesTaches(taches):
    dateTot = datesAuPlusTot(taches)
    dateTard = datesAuPlusTard(taches)

    marges = {}

    for i in taches:
        marges[i]=dateTard[i] - dateTot[i]

    return marges

def tachesCritique(margesTache):

    if
