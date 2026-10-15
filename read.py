def lire_champs(ligne, num_ligne): #verifie que le csv contien 4 champs exactement
    champs = ligne.strip().split(";")
    if len(champs) != 4:
        exit(f"Ligne {num_ligne} : {len(champs)} champs trouvés au lieu de 4.")
    return champs

    ligne=P1.readline()

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