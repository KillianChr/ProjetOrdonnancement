from read import read, inverser
from graphValide import verifier_graphe
from bellman import calculDateAuPlusTot, datesAuPlusTotTacheX

# graphe=read()

nb_task,graphe=read()
graphe_inverse=inverser(graphe, nb_task)

# print(graphe)
if verifier_graphe(graphe):
    calculDateAuPlusTot(graphe)

    # Affiche la date au plus tot de la tache X, il faut que la tache existe sinon clevé de l'erreur
    print(datesAuPlusTotTacheX(5,graphe))
else:
    print("Graphe Invalide")

