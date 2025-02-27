# models.py
from datetime import datetime

class Produit:
    def __init__(self, id_produit, nom, quantite, prix, date_expiration):
        self.id = id_produit
        self.nom = nom
        self.quantite = quantite
        self.prix = prix
        # Conversion de la date en objet datetime pour faciliter les comparaisons
        self.date_expiration = datetime.strptime(date_expiration, "%Y-%m-%d")
    
    def __str__(self):
        return f"Produit({self.id}, {self.nom}, {self.quantite}, {self.prix}, {self.date_expiration.date()})"
