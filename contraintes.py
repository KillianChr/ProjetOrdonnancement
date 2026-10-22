SIGMA = 0  # So : tâche fictive de début de projet (les vraies tâches commencent à 1)


def chevauchement(taches, a, b):
    # NON( Sa + da <= Sb  OU  Sb + db <= Sa )  <=>  Sa + da >= Sb + 1  ET  Sb + db >= Sa + 1
    return [
        (b, a, 1 - taches[a]["duree"]),  # Sa >= Sb + 1 - da
        (a, b, 1 - taches[b]["duree"]),  # Sb >= Sa + 1 - db
    ]


def contraintes(taches):
    # Chaque contrainte "Sj >= Si + q" est un arc (i, j, q)
    return [
        # aucune tâche ne commence avant le début du projet : Si >= So + 0
        *[(SIGMA, i, 0) for i in taches],
        # (S4 >= S1 + S1.durée && S4 >= S2 + S2.durée est dans Graphe/P2.csv : précédentes de 4)
        # S5 >= S3 + 0
        (3, 5, 0),
        # S2 >= So + 3  &&  So >= S2 - 3   (S2 = 3)
        (SIGMA, 2, 3),
        (2, SIGMA, -3),
        # tâches 3 et 4 se chevauchent sur au moins 1 unité de temps
        *chevauchement(taches, 3, 4),
    ]
