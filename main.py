# main.py
from dynamic_array import DynamicArray
from avl_tree import AVLTree
from priority_queue import PriorityQueue
from models import Produit

def menu():
    print("=== Gestionnaire Intelligent de Stocks ===")
    print("1. Ajouter un produit")
    print("2. Modifier un produit")
    print("3. Supprimer un produit")
    print("4. Afficher tous les produits")
    print("5. Rechercher un produit")
    print("6. Afficher file prioritaire (produits en rupture)")
    print("0. Quitter")
    choix = input("Votre choix: ")
    return choix

def main():
    stock = DynamicArray()
    arbre = AVLTree()
    file_prioritaire = PriorityQueue()
    seuil_critique = 5  # Exemple de seuil critique

    while True:
        choix = menu()
        if choix == "1":
            # Ajouter un produit
            id_produit = input("ID: ")
            nom = input("Nom: ")
            quantite = int(input("Quantité: "))
            prix = float(input("Prix: "))
            date_exp = input("Date d'expiration (YYYY-MM-DD): ")
            produit = Produit(id_produit, nom, quantite, prix, date_exp)
            stock.ajouter_produit(produit)
            arbre.inserer(produit)
            file_prioritaire.ajouter(produit, seuil_critique)
        elif choix == "2":
            id_produit = input("ID du produit à modifier: ")
            # Pour simplifier, on demande une nouvelle quantité
            nouvelle_quantite = int(input("Nouvelle quantité: "))
            stock.modifier_produit(id_produit, quantite=nouvelle_quantite)
            
            # Mise à jour dans la file prioritaire
            produit = arbre.rechercher(id_produit)
            if produit:
                file_prioritaire.ajouter(produit, seuil_critique)
        elif choix == "3":
            id_produit = input("ID du produit à supprimer: ")
            stock.supprimer_produit(id_produit)
            
        elif choix == "4":
            stock.afficher_produits()
        elif choix == "5":
            id_produit = input("ID du produit à rechercher: ")
            produit = arbre.rechercher(id_produit)
            if produit:
                print("Produit trouvé :", produit)
            else:
                print("Produit non trouvé.")
        elif choix == "6":
            file_prioritaire.afficher_file()
        elif choix == "0":
            break
        else:
            print("Choix invalide. Réessayez.")

if __name__ == "__main__":
    main()
