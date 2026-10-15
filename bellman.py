from read import read

def datesAuPlusTot(taches):
    # Arcs (i, j, q) : j ne peut pas commencer avant la fin de i, donc q = duree de i
    # j = id de la tache, t = infos de la tâche en question, i = les prédécesseurs de j
    arcs = [(i, j, taches[i]["duree"]) for j, t in taches.items() for i in t["precedente"]]

    s = {i: 0 for i in taches}
    n = len(taches)
    k = 0

    while True:
        k += 1
        c = False
        for i, j, q in arcs:
            if s[j] < s[i] + q:
                s[j] = s[i] + q
                c = True
        if not c or k == n:
            break

    if c: # Si il y a encore des changements après n tours alors levé de l'exception
        raise ValueError("Dépendances circulaires")
    return s

def datesAuPlusTotTacheX(x):
    taches = read()
    if x not in taches:
        raise ValueError(f"La tâche {x} n'existe pas")
    return datesAuPlusTot(taches)[x]

def calculDateAuPlusTot():
    taches = read()
    s = datesAuPlusTot(taches)

    # Test qui affiche chaque tâche avec son début au plus tot
    # for i in taches:
    #     print(f"{i}; {taches[i]['description']}; {s[i]}")

    print("Durée totale :", max(s[i] + taches[i]["duree"] for i in taches))
