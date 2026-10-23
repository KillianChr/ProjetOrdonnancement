"""
Contraintes supplémentaires (au-delà des précédences), valables pour n'importe quel graphe.

Principe du cours (pages 20 à 36) : toute contrainte s'écrit  Sj >= Si + q,
c'est-à-dire un arc (i, j, q) ajouté au graphe. Bellman s'applique ensuite tel quel.
Si les contraintes sont incompatibles, le graphe contient un circuit de longueur
positive et Bellman le détecte (ValueError) : le projet n'est pas réalisable.

Une contrainte est décrite par un dictionnaire (c'est aussi le format envoyé par le site) :
    {"type": "date_fixe", "tacheA": 2, "tacheB": None, "valeur": 3}
"""

SIGMA = 0  # So : tâche fictive de début de projet (les vraies tâches commencent à 1)


def chevauchement(taches, a, b):
    # NON( Sa + da <= Sb  OU  Sb + db <= Sa )  <=>  Sa + da >= Sb + 1  ET  Sb + db >= Sa + 1
    return [
        (b, a, 1 - taches[a]["duree"]),  # Sa >= Sb + 1 - da
        (a, b, 1 - taches[b]["duree"]),  # Sb >= Sa + 1 - db
    ]


# ---------------------------------------------------------------------------
# Un type de contrainte = une fonction (taches, a, b, v) -> liste d'arcs
#   a = tacheA, b = tacheB, v = valeur (0 si non renseignée)
# ---------------------------------------------------------------------------
TYPES = {
    # Sa = v          (ex. P2 : "la tâche 2 commence exactement à la date 3")
    "date_fixe": lambda taches, a, b, v: [(SIGMA, a, v), (a, SIGMA, -v)],

    # Sa >= v         ("a ne peut pas commencer avant la date v")
    "date_min": lambda taches, a, b, v: [(SIGMA, a, v)],

    # Sa <= v         ("a doit avoir commencé à la date v")
    "date_max": lambda taches, a, b, v: [(a, SIGMA, -v)],

    # Sb >= Sa + v    (ex. P2 : "la tâche 5 ne peut commencer avant le début de la tâche 3", v = 0)
    "debut_apres_debut": lambda taches, a, b, v: [(a, b, v)],

    # Sb >= Sa + da + v   (précédence avec un délai de v après la fin de a)
    "debut_apres_fin": lambda taches, a, b, v: [(a, b, taches[a]["duree"] + v)],

    # Sb <= Sa + da + v  <=>  Sa >= Sb - da - v
    # (ex. cours p.20 : "la tâche 6 doit être démarrée au plus 2 jours après la fin de la tâche 3")
    "debut_max_apres_fin": lambda taches, a, b, v: [(b, a, -(taches[a]["duree"] + v))],

    # a et b se chevauchent sur au moins 1 unité de temps (ex. P2 : tâches 3 et 4)
    "chevauchement": lambda taches, a, b, v: chevauchement(taches, a, b),
}

# Types qui ont besoin d'une seconde tâche (tacheB)
TYPES_A_DEUX_TACHES = {"debut_apres_debut", "debut_apres_fin", "debut_max_apres_fin", "chevauchement"}


def arcs_contrainte(taches, contrainte):
    """Transforme UNE contrainte (dictionnaire) en arcs. Lève ValueError si elle est mal formée."""
    type_ = contrainte.get("type")
    a = contrainte.get("tacheA")
    b = contrainte.get("tacheB")
    v = contrainte.get("valeur") or 0

    if type_ not in TYPES:
        raise ValueError(f"Type de contrainte inconnu : {type_}")
    if a not in taches:
        raise ValueError(f"Contrainte '{type_}' : la tâche {a} n'existe pas")
    if type_ in TYPES_A_DEUX_TACHES:
        if b not in taches:
            raise ValueError(f"Contrainte '{type_}' : la seconde tâche {b} n'existe pas")
        if a == b:
            raise ValueError(f"Contrainte '{type_}' : les deux tâches doivent être différentes")

    return TYPES[type_](taches, a, b, int(v))


def contraintes(taches, liste):
    """Arcs de toutes les contraintes d'une liste (sans les précédences, déjà dans le graphe)."""
    return [arc for contrainte in liste for arc in arcs_contrainte(taches, contrainte)]


# Exemple du cours : les contraintes du projet P2 (Graphe/P2.csv), sous forme de données.
# Utilisation : contraintes(graphe_p2, CONTRAINTES_P2)
CONTRAINTES_P2 = [
    # (la tâche 4 après la fin de 1 et 2 est déjà dans Graphe/P2.csv : précédentes de 4)
    {"type": "debut_apres_debut", "tacheA": 3, "tacheB": 5, "valeur": 0},  # S5 >= S3 + 0
    {"type": "date_fixe", "tacheA": 2, "tacheB": None, "valeur": 3},        # S2 = 3
    {"type": "chevauchement", "tacheA": 3, "tacheB": 4, "valeur": None},    # 3 et 4 se chevauchent
]
