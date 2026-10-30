SIGMA = 0  # So : tâche fictive de début de projet (les vraies tâches commencent à 1)

# Chaque contrainte "Sj >= Si + q" est un arc (i, j, q). Chaque fonction renvoie une liste d'arcs.
def precedence(taches, i, j):
    # j ne peut commencer qu'après la fin de i : Sj >= Si + durée(i)
    return [(i, j, taches[i]["duree"])]

def apres_debut(i, j, q=0):
    # j ne peut commencer avant q unités après le début de i : Sj >= Si + q
    return [(i, j, q)]

def date_min(i, d):
    # i commence au plus tôt à la date d : Si >= So + d
    return [(SIGMA, i, d)]

def date_max(i, d):
    # i commence au plus tard à la date d : Si <= So + d  <=>  So >= Si - d
    return [(i, SIGMA, -d)]

def date_fixe(i, d):
    # i commence exactement à la date d
    return date_min(i, d) + date_max(i, d)

def chevauchement(taches, a, b):
    # NON( Sa + da <= Sb  OU  Sb + db <= Sa )  <=>  Sa + da >= Sb + 1  ET  Sb + db >= Sa + 1
    return [
        (b, a, 1 - taches[a]["duree"]),  # Sa >= Sb + 1 - da
        (a, b, 1 - taches[b]["duree"]),  # Sb >= Sa + 1 - db
    ]


def contraintes_P1(taches):
    return []  # P1 n'a que les précédences du CSV


def contraintes_P2(taches):
    return [
        # aucune tâche ne commence avant le début du projet : Si >= So + 0
        *[(SIGMA, i, 0) for i in taches],
        # (la tâche 4 après la fin de 1 et 2 est dans Graphe/P2.csv : précédentes de 4)
        *apres_debut(3, 5),          # la tâche 5 ne commence pas avant le début de 3
        *date_fixe(2, 3),            # la tâche 2 commence exactement à la date 3
        *chevauchement(taches, 3, 4),  # 3 et 4 se chevauchent sur au moins 1 unité
        # ajoute ici une ligne par nouvelle contrainte
    ]


def contraintes(chemin, taches):
    # choisit les contraintes d'après le nom du CSV ("Graphe/P2.csv" -> P2) ; sans contraintes si inconnu
    nom = chemin.replace("\\", "/").split("/")[-1].removesuffix(".csv")
    return {"P1": contraintes_P1, "P2": contraintes_P2}.get(nom, contraintes_P1)(taches)
