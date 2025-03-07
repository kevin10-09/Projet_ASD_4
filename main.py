from dynamic_array import DynamicArray
from avl_tree import AVLTree
from priority_queue import PriorityQueue
from models import Produit
from datetime import datetime

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
            try:
                id_produit = input("ID: ")
                nom = input("Nom: ")
                quantite = int(input("Quantité: "))
                prix = float(input("Prix: "))
                date_exp = input("Date d'expiration (YYYY-MM-DD): ")
                
                # Validation de la date
                try:
                    datetime.strptime(date_exp, "%Y-%m-%d")
                except ValueError:
                    print("Erreur: Format de date invalide. Utilisez 'YYYY-MM-DD'.")
                    continue

                produit = Produit(id_produit, nom, quantite, prix, date_exp)
                stock.ajouter_produit(produit)
                arbre.inserer(produit)
                file_prioritaire.ajouter(produit, seuil_critique)
                print("Produit ajouté avec succès!")
            except ValueError as e:
                print(f"Erreur: {str(e)}")
            except Exception as e:
                print(f"Une erreur inattendue s'est produite: {str(e)}")

        elif choix == "2":
            # Modifier un produit
            try:
                id_produit = input("ID du produit à modifier: ")
                nouvelle_quantite = int(input("Nouvelle quantité: "))
                stock.modifier_produit(id_produit, quantite=nouvelle_quantite)
                
                # Mise à jour dans la file prioritaire
                produit = arbre.rechercher(id_produit)
                if produit:
                    file_prioritaire.ajouter(produit, seuil_critique)
                print("Produit modifié avec succès!")
            except ValueError as e:
                print(f"Erreur: {str(e)}")
            except Exception as e:
                print(f"Une erreur inattendue s'est produite: {str(e)}")

        elif choix == "3":
            # Supprimer un produit
            try:
                id_produit = input("ID du produit à supprimer: ")
                stock.supprimer_produit(id_produit)
                print("Produit supprimé avec succès!")
            except ValueError as e:
                print(f"Erreur: {str(e)}")
            except Exception as e:
                print(f"Une erreur inattendue s'est produite: {str(e)}")

        elif choix == "4":
            # Afficher tous les produits
            try:
                print(stock.afficher_produits())
            except Exception as e:
                print(f"Erreur lors de l'affichage des produits: {str(e)}")

        elif choix == "5":
            # Rechercher un produit
            try:
                id_produit = input("ID du produit à rechercher: ")
                produit = arbre.rechercher(id_produit)
                if produit:
                    print("Produit trouvé :", produit)
                else:
                    print("Produit non trouvé.")
            except Exception as e:
                print(f"Erreur lors de la recherche du produit: {str(e)}")

        elif choix == "6":
            # Afficher la file prioritaire
            try:
                print(file_prioritaire.afficher_file())
            except Exception as e:
                print(f"Erreur lors de l'affichage de la file prioritaire: {str(e)}")

        elif choix == "0":
            # Quitter
            print("Merci d'avoir utilisé le Gestionnaire de Stocks. Au revoir!")
            break

        else:
            print("Choix invalide. Réessayez.")

if __name__ == "__main__":
    main()