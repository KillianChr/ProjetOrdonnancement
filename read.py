def lire_champs(ligne, num_ligne): #verifie que le csv contien 4 champs exactement
    champs = ligne.strip().split(";")
    if len(champs) != 4:
        exit(f"Ligne {num_ligne} : {len(champs)} champs trouvés au lieu de 4.")
    return champs

def verifier_tache(champs, num_ligne): #verifie que le csv est en Chiffre;Nom;Chiffre;Chiffre
    id, description, duree, precedentes = champs

    if not id.isdigit():
        exit(f"Ligne {num_ligne} : l'ID '{id}' n'est pas un nombre.")
    if not description.isalpha():
        exit(f"Ligne {num_ligne} : la description '{description}' est invalide.")
    if not duree.isdigit():
        exit(f"Ligne {num_ligne} : la durée '{duree}' n'est pas un nombre.")
    if precedentes and not all(p.strip().isdigit() for p in precedentes.split(",")): #Verifie que les predecesseurs sont des nombres même si il y en a pas ou plusieurs
        exit(f"Ligne {num_ligne} : prédécesseurs invalides '{precedentes}'.")


def read(chemin="Graphe/P1.csv"):
    with open(chemin) as csvfile:
        premiere = csvfile.readline().strip()
        if not premiere.isdigit():
            exit("Le nombre de tache du CSV n'est pas indiqué")
        nb_task = int(premiere) #Passage obligatoire en int sinon le range marche pas car il ne peut pas compter un string

        lire_champs(csvfile.readline(), 2)  # en-tête (qui ne sert a rien au passage)

        graphe = {}
        for i in range(nb_task):
            champs = lire_champs(csvfile.readline(), i + 3) # +3 parce graphe commence a ligne 3
            verifier_tache(champs, i + 3)  
            id, description, duree, precedentes = champs
            graphe[int(id)] = {
                "description": description,
                "duree": int(duree),
                "precedente": [int(p) for p in precedentes.split(",") if p], #Permet de mettre TOUT les predecesseurs soit mise dans une liste même si il n'y en a pas (if p)
            }

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
