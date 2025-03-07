from datetime import datetime

class Produit:
    def __init__(self, id_produit, nom, quantite, prix, date_expiration):
        # Validation de l'ID
        if not isinstance(id_produit, str) or not id_produit.strip() or not id_produit.isdigit() or int(id_produit) <= 0 :
            raise ValueError("L'ID du produit doit être une chaîne non vide.")

        # Validation du nom
        if not isinstance(nom, str) or not nom.strip():
            raise ValueError("Le nom du produit doit être une chaîne non vide.")

        # Validation de la quantité
        if not isinstance(quantite, int) or quantite < 0:
            raise ValueError("La quantité doit être un entier positif.")

        # Validation du prix
        if not isinstance(prix, (int, float)) or prix < 0:
            raise ValueError("Le prix doit être un nombre positif.")

        # Validation de la date d'expiration
        try:
            self.date_expiration = datetime.strptime(date_expiration, "%Y-%m-%d")
            if self.date_expiration < datetime.now():
                raise ValueError("La date d'expiration doit être dans le futur.")
        except ValueError:
            raise ValueError("Format de date invalide. Utilisez 'YYYY-MM-DD'.")

        self.id = id_produit
        self.nom = nom
        self.quantite = quantite
        self.prix = prix

    def __str__(self):
        return f"Produit(ID: {self.id}, Nom: {self.nom}, Quantité: {self.quantite}, Prix: {self.prix}, Expiration: {self.date_expiration.strftime('%Y-%m-%d')})"