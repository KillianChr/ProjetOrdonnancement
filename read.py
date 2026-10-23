def lire_champs(ligne, num_ligne): #verifie que le csv contien 4 champs exactement
    champs = ligne.strip().split(";")
    if len(champs) != 4:
        exit(f"Ligne {num_ligne} : {len(champs)} champs trouvés au lieu de 4.")
    return champs

def verifier_tache(champs, num_ligne): #verifie que le csv est en Chiffre;Nom;Chiffre;Chiffre
    id, description, duree, precedentes = champs

    if not id.isdigit():
        exit(f"Ligne {num_ligne} : l'ID '{id}' n'est pas un nombre.")
    # La description sert seulement à l'affichage : on accepte tout texte non vide
    # (espaces, accents, chiffres…). Le ";" est de toute façon impossible car il sépare les champs.
    if not description.strip():
        exit(f"Ligne {num_ligne} : la description est vide.")
    if not duree.isdigit():
        exit(f"Ligne {num_ligne} : la durée '{duree}' n'est pas un nombre.")
    if precedentes and not all(p.strip().isdigit() for p in precedentes.split(",")): #Verifie que les predecesseurs sont des nombres même si il y en a pas ou plusieurs
        exit(f"Ligne {num_ligne} : prédécesseurs invalides '{precedentes}'.")


def ouvrir_csv(chemin): #renvoie la liste des lignes du fichier
    # On essaie d'abord l'UTF-8 ("-sig" ignore le BOM ajouté par Excel en "CSV UTF-8"),
    # sinon on retombe sur l'encodage Windows d'Excel (cp1252, le "CSV point-virgule" classique)
    try:
        with open(chemin, encoding="utf-8-sig") as f:
            return f.read().splitlines()
    except UnicodeDecodeError:
        with open(chemin, encoding="cp1252") as f:
            return f.read().splitlines()


def read(chemin):
    lignes = ouvrir_csv(chemin)

    # ligne(n) renvoie la n-ième ligne du fichier (en partant de 1), ou "" si le fichier est trop court
    ligne = lambda n: lignes[n - 1] if n <= len(lignes) else ""

    premiere = ligne(1).strip()
    if not premiere.isdigit():
        exit("Le nombre de tache du CSV n'est pas indiqué")
    nb_task = int(premiere) #Passage obligatoire en int sinon le range marche pas car il ne peut pas compter un string

    lire_champs(ligne(2), 2)  # en-tête (qui ne sert a rien au passage)

    graphe = {}
    for i in range(nb_task):
        champs = lire_champs(ligne(i + 3), i + 3) # +3 parce graphe commence a ligne 3
        verifier_tache(champs, i + 3)
        id, description, duree, precedentes = champs
        if int(id) in graphe:
            exit(f"Ligne {i + 3} : l'ID {id} est déjà utilisé par une autre tâche.")
        graphe[int(id)] = {
            "description": description.strip(),
            "duree": int(duree),
            "precedente": [int(p) for p in precedentes.split(",") if p], #Permet de mettre TOUT les predecesseurs soit mise dans une liste même si il n'y en a pas (if p)
        }

    # Le cours impose des tâches numérotées 1, 2, …, n (V = {1..n}) ; inverser() en dépend aussi
    if sorted(graphe) != list(range(1, nb_task + 1)):
        exit(f"Les ID des tâches doivent aller de 1 à {nb_task}, sans trou.")

    # Lignes en trop après les nb_task tâches annoncées (les lignes vides en fin de fichier sont tolérées)
    if any(l.strip() for l in lignes[2 + nb_task:]):
        exit(f"Le fichier contient plus de {nb_task} tâches (nombre annoncé en 1re ligne).")

    return nb_task, graphe

def inverser(graphe, nb): #Inverse Strictement le graphe (même les 'precedente')
    nouveau = lambda t: nb + 1 - t 

    #Inversion total du graphe sans les 'precendente' en fonction de lambda du graphe
    inverse = {
        nouveau(t): {
            'description': graphe[t]['description'],
            'duree': graphe[t]['duree'],
            'precedente': [],
        }
        for t in sorted(graphe, reverse=True) #Remet les id dans l'odre voulu
    }
    #Inverse les 'precedente' en fonction de t & p (a retenir 'nouveau' est l'inverse exact)
    #sur on regarde la case graphe.id =10 alors nouveau(10) = 1 donc id =1 nouveau(6) = 5
    for t, info in graphe.items():
        for p in info['precedente']:
            inverse[nouveau(p)]['precedente'].append(nouveau(t))

    for info in inverse.values(): #Sert peut-être (JSP comment le script de bellman fonctionne exactement)
        info['precedente'].sort() #Sinon cela sert juste a remettre les 'precedente' dnas l'ordre croissant
    return inverse
