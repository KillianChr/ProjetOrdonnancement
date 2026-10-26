def ouvrir_csv(chemin):
    try:
        with open(chemin, encoding="utf-8-sig") as l: 
            return l.readlines()
    except UnicodeDecodeError:
        with open(chemin, encoding="cp1252") as l:
            return l.readlines()

def verifier(ligne, num_ligne): #verifie que le csv est en Chiffre;Nom;Chiffre;Chiffre
    champs = ligne.strip().split(";")
    if len(champs) != 4:
        exit(f"Ligne {num_ligne} : {len(champs)} champs trouvés au lieu de 4.")
    id, description, duree, precedentes = champs
    if not id.isdigit():
        exit(f"Ligne {num_ligne} : l'ID '{id}' n'est pas un nombre.")
    if not description:
        exit(f"Ligne {num_ligne} : la description '{description}' est invalide.")
    if not duree.isdigit():
        exit(f"Ligne {num_ligne} : la durée '{duree}' n'est pas un nombre.")
    if precedentes and not all(p.strip().isdigit() for p in precedentes.split(",")): #Verifie que les predecesseurs sont des nombres même si il y en a pas ou plusieurs
        exit(f"Ligne {num_ligne} : prédécesseurs invalides '{precedentes}'.")
    return champs


def read(chemin):
    lignes = iter(ouvrir_csv(chemin)) #"iter" permet de de faire un "next" pour la lecture des lignes
    
    premiere = next(lignes).strip()
    if not premiere.isdigit():
        exit("Le nombre de tache du CSV n'est pas indiqué")
    nb_task = int(premiere) #Passage obligatoire en int sinon le range marche pas car il ne peut pas compter un string

    Sert_a_rien = next(lignes)  #Cette ligne ne sert littérallement à rien appart m'embetter

    graphe = {}
    for i in range(nb_task):

        ligne = next(lignes, None)
        if ligne is None and not ligne:
            exit(f"{nb_task} tâches sont annoncées seulement il n'y a que {i} tâches")

        champs = verifier(ligne, i + 3) # +3 parce graphe commence a ligne 3
        id, description, duree, precedentes = champs

        if int(id) in graphe: #Verif des doublon
            exit(f"Ligne {i+3} : l'ID '{id}' est en doublon.")

        graphe[int(id)] = {
            "description": description,
            "duree": int(duree),
            "precedente": [int(p) for p in precedentes.split(",") if p], #Permet de mettre TOUT les predecesseurs soit mise dans une liste même si il n'y en a pas (if p)
        }

    if set(graphe) != set(range(1, nb_task + 1)): #Permet de vérifier les trou dans le graphe
        exit(f"Les ID ne vont pas de 1 à {nb_task}")

    for nb in enumerate(lignes, start=nb_task+3): #Verifie si il y moins de lignes qu'annoncées
        if nb != nb_task:
            exit(f"Il y a plus de {nb_task} lignes")

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
