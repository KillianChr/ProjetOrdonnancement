
from read import read, inverser
from graphValide import verifier_graphe
from ordonnancement import dureeProjet, datesTacheX , datesAuPlusTard , datesAuPlusTot

nb_task, graphe = read()
graphe_inverse = inverser(graphe, nb_task)
dateAuPlusTard = datesAuPlusTard(graphe)

if verifier_graphe(graphe):
    print("Durée totale :", dureeProjet(graphe))
    print(datesTacheX(7,graphe,datesAuPlusTot))
    print(datesTacheX(7,graphe,datesAuPlusTard))

else:
    print("Graphe invalide")
