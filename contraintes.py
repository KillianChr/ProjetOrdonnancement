import sys

from read import read

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


# Fonctions utilisables dans les fichiers de contraintes (Graphe/Pn.contraintes.csv)
FONCTIONS = {f.__name__: f for f in (precedence, apres_debut, date_min, date_max, date_fixe, chevauchement)}
AVEC_TACHES = {"precedence", "chevauchement"}  # ces fonctions reçoivent aussi `taches`


def fichier_contraintes(chemin):
    return chemin.removesuffix(".csv") + ".contraintes.csv"  # "Graphe/P2.csv" -> "Graphe/P2.contraintes.csv"


def arcs_contrainte(nom, params, taches):
    # transforme une contrainte (nom + paramètres) en arcs, en vérifiant qu'elle est valide
    if nom not in FONCTIONS:
        raise ValueError(f"Contrainte inconnue '{nom}' (disponibles : {', '.join(FONCTIONS)})")
    args = (taches, *params) if nom in AVEC_TACHES else tuple(params)
    try:
        arcs = FONCTIONS[nom](*args)
    except TypeError:
        raise ValueError(f"Mauvais nombre de paramètres pour '{nom}'")
    except KeyError as e:  # ex : precedence() sur une tâche absente du CSV
        raise ValueError(f"Contrainte sur une tâche inexistante : {e}")
    for i, j, q in arcs:
        for x in (i, j):
            if x != SIGMA and x not in taches:
                raise ValueError(f"Contrainte sur une tâche inexistante : {x}")
    return arcs


def contraintes(chemin, taches):
    # lit Graphe/Pn.contraintes.csv (une contrainte par ligne : nom;param;param...) et renvoie tous les arcs
    arcs = [(SIGMA, i, 0) for i in taches]  # aucune tâche ne commence avant le début du projet
    fichier = fichier_contraintes(chemin)
    try:
        with open(fichier, encoding="utf-8-sig") as f:
            lignes = f.readlines()
    except FileNotFoundError:
        return arcs  # pas de fichier = pas de contraintes supplémentaires
    for n, ligne in enumerate(lignes, 1):
        if not ligne.strip():
            continue
        nom, *params = ligne.strip().split(";")
        try:
            arcs += arcs_contrainte(nom, [int(p) for p in params], taches)
        except ValueError as e:
            raise ValueError(f"{fichier}, ligne {n} : {e}")
    return arcs


def ajouter_contrainte(chemin, nom, *params):
    # ajoute une contrainte dans le fichier de contraintes du projet, après vérification
    # ex : ajouter_contrainte("Graphe/P3.csv", "date_max", 3, 9)
    _, taches = read(chemin)
    arcs_contrainte(nom, params, taches)  # lève ValueError si la contrainte est invalide
    ligne = ";".join([nom, *map(str, params)])
    fichier = fichier_contraintes(chemin)
    try:
        with open(fichier, encoding="utf-8-sig") as f:
            texte = f.read()
    except FileNotFoundError:
        texte = ""
    if ligne in texte.splitlines():
        return  # déjà présente
    with open(fichier, "a", encoding="utf-8") as f:
        f.write(("\n" if texte and not texte.endswith("\n") else "") + ligne + "\n")


if __name__ == "__main__":
    # python contraintes.py P3 date_max 3 9
    ajouter_contrainte(f"Graphe/{sys.argv[1]}.csv", sys.argv[2], *map(int, sys.argv[3:]))
