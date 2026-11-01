# ProjetOrdonnancement

Outil de planification de projet par la **méthode des potentiels**. À partir d'une liste de tâches, de leurs durées, de leurs précédences et de contraintes supplémentaires, il vérifie que le projet est réalisable, puis calcule avec l'algorithme de Bellman :

- la durée minimale du projet ;
- les dates de début au plus tôt et au plus tard de chaque tâche ;
- les marges et les tâches critiques.

Le projet a deux parties : les **calculs en Python** à la racine, et une **interface web Symfony** dans `web/`, qui utilise ces calculs.

## Prérequis

- **Calculs** : Python 3, sans dépendance externe.
- **Interface web** : PHP 8.5 ou plus récent, avec l'extension `pdo_sqlite`, et Composer. Le [CLI Symfony](https://symfony.com/download) est facultatif.

## Utiliser les calculs Python

Depuis la racine du projet :

```bash
python index.py        # projet P1 par défaut
python index.py P2     # lit Graphe/P2.csv et Graphe/P2.contraintes.csv
```

Le résultat est écrit dans `resultat.json` : durée du projet, puis dates, marge et statut critique de chaque tâche. Si le projet n'est pas réalisable, `realisable` vaut `false` et `erreur` donne la raison.

Pour ajouter une contrainte au fichier d'un projet :

```bash
python contraintes.py P3 date_max 3 9
```

## Utiliser l'interface web

Première installation :

```bash
cd web
composer install
php bin/console doctrine:migrations:migrate
```

Lancement, depuis `web/` :

```bash
symfony serve
# ou, sans le CLI Symfony :
php -S 127.0.0.1:8000 -t public
```

L'interface permet de créer et modifier des projets, des tâches et des contraintes. Le planning, les marges et le chemin critique sont recalculés à chaque affichage. Les données sont stockées dans une base SQLite (`web/var/data.db`), séparée des fichiers de `Graphe/`.

Si la commande `python` n'est pas disponible, indiquez le bon exécutable dans `PYTHON_BIN`, par exemple dans un fichier `web/.env.local`, qui ne doit jamais être commité.

## Format des fichiers

### Tâches : `Graphe/Pn.csv`

Séparateur : `;`.

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
| 2 | En-tête (ignoré) |
| 3 et suivantes | `id;description;durée;précédentes` |

- **ID** : ils vont exactement de 1 au nombre de tâches, sans trou ni doublon.
- **Description** : elle ne doit pas être vide.
- **Précédentes** : identifiants des tâches à terminer avant, séparés par `,` (ex. `1,2`). Vide si aucune.
- **Encodage** : UTF-8 ou cp1252 (l'encodage Windows d'Excel).

### Contraintes : `Graphe/Pn.contraintes.csv`

Fichier facultatif, avec une contrainte par ligne : `nom;paramètre;paramètre...`

```
apres_debut;3;5
date_fixe;2;3
chevauchement;3;4
```

| Contrainte | Signification |
|---|---|
| `precedence;i;j` | j commence après la fin de i |
| `apres_debut;i;j;q` | j ne commence pas avant q unités après le début de i (q vaut 0 s'il est omis) |
| `date_min;i;d` | i commence au plus tôt à la date d |
| `date_max;i;d` | i commence au plus tard à la date d |
| `date_fixe;i;d` | i commence exactement à la date d |
| `chevauchement;a;b` | a et b se chevauchent sur au moins 1 unité de temps |

L'interface web propose ces six types, plus un septième : `debut_max_apres_fin` (B commence au plus X après la fin de A, exemple de la page 20 du cours).

Chaque contrainte s'écrit `Sj >= Si + q`, c'est-à-dire un arc ajouté au graphe. Si les contraintes se contredisent, Bellman détecte un circuit de longueur positive et le projet est déclaré non réalisable.

## Structure du projet

| Fichier | Rôle |
|---|---|
| `index.py` | Point d'entrée en ligne de commande, écrit `resultat.json` |
| `calcul.py` | Regroupe les calculs d'un projet ; pont avec l'interface web (JSON en entrée et en sortie) |
| `read.py` | Lecture et validation du CSV, inversion du graphe (`inverser()`) |
| `graphValide.py` | Vérification du graphe : tâche de départ, précédentes existantes, durées positives, absence de cycle |
| `contraintes.py` | Contraintes supplémentaires, traduites en arcs ; lecture et ajout dans les fichiers de contraintes |
| `bellman.py` | Algorithme de Bellman : `bellman_inverse` (plus longs chemins, dates au plus tôt) et `bellman` (plus courts chemins, dates au plus tard) |
| `ordonnancement.py` | Dates au plus tôt et au plus tard, durée du projet, marges, tâches critiques |
| `Graphe/` | Projets d'exemple |
| `Support D1-36.pdf` | Support de cours |
| `web/` | Interface Symfony : entités `Projet`, `Tache`, `Contrainte`, formulaires et pages |

Tous les calculs d'ordonnancement sont faits en Python. Le service `web/src/Service/CalculOrdonnancement.php` lance `calcul.py`, lui envoie le projet en JSON et récupère le résultat.

## Travail en équipe

Chaque membre travaille sur sa branche, et `main` reste la version stable.

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
