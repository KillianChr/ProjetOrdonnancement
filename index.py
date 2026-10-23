
from read import read, inverser
from graphValide import verifier_graphe
from ordonnancement import dureeProjet, datesTacheX , datesAuPlusTard , datesAuPlusTot , margesTaches, tachesCritique 

nb_task, graphe = read()
graphe_inverse = inverser(graphe, nb_task)

if verifier_graphe(graphe):
    #initialisation 
    duree = dureeProjet(graphe)
    dates_tot = datesAuPlusTot(graphe)
    dates_tard = datesAuPlusTard(graphe)
    marges = margesTaches(graphe)
    critiques = tachesCritique(marges)

    resultat = {
        "realisable": True,
        "duree_projet": duree,
        "taches": {
            "dates_au_plus_tot": dates_tot,
            "dates_au_plus_tard": dates_tard,
            "marges": marges,
            "taches_critiques": critiques
        }
    }



else:
    print("Graphe invalide")
