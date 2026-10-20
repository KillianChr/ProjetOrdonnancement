# ProjetOrdonnancement

Outil d'ordonnancement de tâches : à partir d'une liste de tâches avec leurs durées et leurs contraintes d'antériorité, le programme vérifie la validité du graphe des tâches (dépendances circulaires, tâches inexistantes, durées) puis calcule les dates au plus tôt (algorithme de Bellman) et la durée totale du projet.

## Prérequis

- Python 3 (aucune dépendance externe, bibliothèque standard uniquement)

## Lancer le programme

Depuis la racine du projet :

```bash
python index.py
```

> Le chemin `Graphe/P1.csv` est relatif : le programme doit être lancé depuis la racine.

## Format du fichier CSV

Les graphes sont dans le dossier `Graphe/`. Séparateur : `;`.

```
10
ID;Description;Duree;Precedentes
1;Murs;7;
2;Charpente;3;1
3;Toiture;1;2
```

| Ligne | Contenu |
|---|---|
| 1 | Nombre de tâches |
| 2 | En-tête (4 colonnes) |
| 3+ | `id;description;durée;précédentes` |

- **Précédentes** : identifiants des tâches à terminer avant, séparés par `,` (ex. `1,2`). Vide si aucune.

## Structure du projet

| Fichier | Rôle |
|---|---|
| `index.py` | Point d'entrée |
| `read.py` | Lecture et validation du CSV (`read()`), inversion du graphe (`inverser()`) |
| `graphValide.py` | Vérification du graphe : cycles, précédentes existantes, durées positives |
| `bellman.py` | Algorithme de Bellman (plus longs chemins) |
| `ordonnancement.py` | Dates au plus tôt, date au plus tôt d'une tâche, durée du projet |
| `Graphe/` | Fichiers CSV d'exemple |
| `Support D1-14.pdf` | Support de cours |

`read()` renvoie le nombre de tâches et le graphe :

```python
nb_task, graphe = read()
# graphe :
{
    1: {"description": "Murs", "duree": 7, "precedente": []},
    2: {"description": "Charpente", "duree": 3, "precedente": [1]},
}
```

## Travail en équipe

Chaque membre travaille sur sa branche : `gabriel`, `theo`, `killian`. `main` reste la version stable.

```bash
git switch <ma-branche>
git pull origin main        # récupérer les dernières nouveautés
# ... coder ...
git add .
git commit -m "feat: description courte"
git push
```

Une fois une fonctionnalité terminée : ouvrir une Pull Request de sa branche vers `main` sur GitHub, à faire relire par un autre membre.

**Convention de commits** : [Conventional Commits](https://www.conventionalcommits.org/fr/) en français (`feat:`, `fix:`, `docs:`, `chore:`…).

## Équipe

Gabriel · Yoan · Théo · Killian
