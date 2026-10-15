import csv
from graphlib import CycleError,TopologicalSorter

# Vérification de la validité du graph

def verifier_graphe(graphe):  
    try:
        #
        
        precedente = {}
        tacheInitial = False

        for i in graphe :
            lprec=graphe[i]["precedente"]
            precedente[i]=lprec

            #minimum une tache sans precedente
            if not lprec:
                tacheInitial=True
                
            #valeur precedente = tache existante
            for j in range(len(lprec)):
                if lprec[j] not in graphe:
                    return False
                
            #duree entier positif
            if graphe[i]["duree"] <= 0:
                return False
                
        TopologicalSorter(precedente).static_order()

        if not tacheInitial:
            return False

        return True
        
    except CycleError as e:
        print("Erreur : dépendances circulaires ->", e.args[1])
        return False
    except (KeyError, TypeError):
        return False
