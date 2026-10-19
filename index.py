
from read import read, inverser
from graphValide import verifier_graphe
from ordonnancement import dureeProjet, datesAuPlusTotTacheX

nb_task, graphe = read()
graphe_inverse = inverser(graphe, nb_task)

if verifier_graphe(graphe):
    print("Durée totale :", dureeProjet(graphe))
    print(datesAuPlusTotTacheX(5, graphe))
else:
    print("Graphe invalide")
