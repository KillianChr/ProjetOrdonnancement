def lire_champs(ligne): #verifie que le csv contien 4 champs
    champs = ligne.strip().split(";")
    if len(champs) != 4:
        exit("Erreur dans le fichier CSV.")
    return champs

def verifier_tache(champs, num_ligne): #verifie que le csv est en Chiffre;Nom;Chiffre;Chiffre
    id_, description, duree, precedentes = champs

    if not id_.isdigit():
        exit(f"Ligne {num_ligne} : l'ID '{id_}' n'est pas un nombre.")
    if not description.isalpha():
        exit(f"Ligne {num_ligne} : la description '{description}' est invalide.")
    if not duree.isdigit():
        exit(f"Ligne {num_ligne} : la durée '{duree}' n'est pas un nombre.")
    if precedentes and not all(p.strip().isdigit() for p in precedentes.split(",")):
        exit(f"Ligne {num_ligne} : prédécesseurs invalides '{precedentes}'.")


def read(chemin="Graphe/P1.csv"):
    with open(chemin) as csvfile:
        premiere = csvfile.readline().strip()
        if not premiere.isdigit():
            exit("Le nombre de tache du CSV n'est pas indiqué")
        nb_task = int(premiere)

        lire_champs(csvfile.readline())  # en-tête

        graphe = {}
        for i in range(nb_task):
            champs = lire_champs(csvfile.readline())
            verifier_tache(champs, i + 3)  # +3 parce graphe commence a ligne 3
            id_, description, duree, precedentes = champs
            graphe[int(id_)] = {
                "description": description,
                "duree": int(duree),
                "precedente": [int(p) for p in precedentes.split(",") if p], #Je vais pas mentir cette ligne était hard
            }

    return nb_task, graphe