from read import read 
from bellman import calculDateAuPlusTot, datesAuPlusTotTacheX

# graphe=read()

# print(graphe)

calculDateAuPlusTot()

# Affiche la date au plus tot de la tache X, il faut que la tache existe sinon clevé de l'erreur
print(datesAuPlusTotTacheX(5))