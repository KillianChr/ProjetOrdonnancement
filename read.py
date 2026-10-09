def read():
    P1=open("Graphe/P1.csv")

    ligne=P1.readline()

    #recuperer la premiere ligne du csv
    if not ligne.strip().isdigit() :
        print("Le nombre de tache du CSV n'est pas indiqué")
        exit()
    nb_task =  int(ligne.strip())

    #Vérification en-tête
    ligne=P1.readline()
    if (len(ligne.strip().split(";")) != 4) : 
        print ("Erreur dans le fichier CSV.")
        exit()
    graphe={}
    #verifier le nombre de champ par ligne
    for i in  range (nb_task) :
        ligne=P1.readline()
        if (len(ligne.strip().split(";")) != 4) : 
            print ("Erreur dans le fichier CSV.")
            exit()
        champ = ligne.strip().split(";")
        precedente=champ[3].strip().split(",")
        liste_champ3=[]
        
        for j in range (len(precedente)) :
            if precedente[j] == "" :
                pass
            else :
                liste_champ3.append(int(precedente[j]))
            
        graphe[int(champ[0])] = {"description":champ[1], 
                                "duree":int(champ[2]), 
                                "precedente":liste_champ3 
                                }

    return graphe


    
