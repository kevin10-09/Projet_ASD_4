from datetime import datetime

class DynamicArray:
    def __init__(self):
        self.array = []  # Tableau dynamique pour stocker les produits

    def ajouter_produit(self, produit):
        """
        Ajoute un produit au tableau dynamique.
        Vérifie que les données sont valides.
        """
        # Vérifier que l'ID est unique
        if any(p.id == produit.id for p in self.array):
            raise ValueError(f"Un produit avec l'ID {produit.id} existe déjà.")

    # Ajouter le produit au tableau
        self.array.append(produit)    
    def modifier_produit(self, id_produit, **kwargs):
        """
        Modifie les informations d'un produit existant.
        Vérifie que le produit existe et que les nouvelles données sont valides.
        """
        produit_trouve = None

        # Recherche du produit dans la liste
        for produit in self.array:
            if produit.id == id_produit:
                produit_trouve = produit
                break

        if not produit_trouve:
            raise ValueError(f"Produit avec l'ID {id_produit} introuvable.")

        # Mise à jour des champs avec validation
        if 'nom' in kwargs:
            if not isinstance(kwargs['nom'], str) or not kwargs['nom'].strip():
                raise ValueError("Le nom du produit doit être une chaîne non vide.")
            produit_trouve.nom = kwargs['nom']

        if 'quantite' in kwargs:
            if not isinstance(kwargs['quantite'], int) or kwargs['quantite'] < 0:
                raise ValueError("La quantité doit être un entier positif.")
            produit_trouve.quantite = kwargs['quantite']

        if 'prix' in kwargs:
            if not isinstance(kwargs['prix'], (int, float)) or kwargs['prix'] < 0:
                raise ValueError("Le prix doit être un nombre positif.")
            produit_trouve.prix = kwargs['prix']

        if 'date_expiration' in kwargs:
            try:
                date_expiration = datetime.strptime(kwargs['date_expiration'], "%Y-%m-%d")
                if date_expiration < datetime.now():
                    raise ValueError("La date d'expiration doit être dans le futur.")
                produit_trouve.date_expiration = date_expiration
            except ValueError:
                raise ValueError("Format de date invalide. Utilisez 'YYYY-MM-DD'.")

        return produit_trouve  # Retourne le produit mis à jour

    def supprimer_produit(self, id_produit):
        """
        Supprime un produit du tableau dynamique.
        """
        # Vérifier si l'ID existe dans la liste
        if not any(p.id == id_produit for p in self.array):
            raise ValueError(f"Aucun produit avec l'ID {id_produit} n'existe.")
    
        # Supprimer le produit si l'ID existe
        self.array = [p for p in self.array if p.id != id_produit]


    def afficher_produits(self):
        """
        Affiche la liste des produits sous forme de chaîne formatée.
        """
        if not self.array:
            print("Aucun produit en stock.")
        else:
            for produit in self.array:
                print(produit)