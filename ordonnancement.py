
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


def datesAuPlusTotTacheX(x, taches):
    if x not in taches:
        raise ValueError(f"La tâche {x} n'existe pas")

    return datesAuPlusTot(taches)[x]


def dureeProjet(taches):
    s = datesAuPlusTot(taches)

    return max(
        s[i] + taches[i]["duree"]
        for i in taches
    )
