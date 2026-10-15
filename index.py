from read import read 
from bellman import calculDateAuPlusTot, datesAuPlusTotTacheX

nb_grahpe, graphe=read()

print(graphe)
print(nb_grahpe)
calculDateAuPlusTot()

# Affiche la date au plus tot de la tache X, il faut que la tache existe sinon clevé de l'erreur
# print(datesAuPlusTotTacheX(5))
