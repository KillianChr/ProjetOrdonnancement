
from read import read, inverser
from graphValide import verifier_graphe
from ordonnancement import dureeProjet, datesTacheX , datesAuPlusTard , datesAuPlusTot , margesTaches, tachesCritique 

nb_task, graphe = read()
graphe_inverse = inverser(graphe, nb_task)
dateAuPlusTard = datesAuPlusTard(graphe)

if verifier_graphe(graphe):
    print("Durée totale :", dureeProjet(graphe))
    print("Date au plus tôt (tache 7):",datesTacheX(7,graphe,datesAuPlusTot))
    print("Date au plus tard (tache 7):", datesTacheX(7,graphe,datesAuPlusTard))
    print("Taches Critique : ", tachesCritique(margesTaches(graphe)))

else:
    print("Graphe invalide")
