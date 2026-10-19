from read import read
from graphValide import verifier_graphe
from ordonnancement import dureeProjet, datesAuPlusTotTacheX

nb_task, graphe = read()

if verifier_graphe(graphe):
    print("Durée totale :", dureeProjet(graphe))

    # Affiche la date au plus tôt de la tâche X
    print(datesAuPlusTotTacheX(5, graphe))
else:
    print("Graphe Invalide")
