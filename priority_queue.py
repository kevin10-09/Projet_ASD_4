# priority_queue.py
import heapq

class PriorityQueue:
    def __init__(self):
        self.tas = []
    
    def ajouter(self, produit, seuil_critique):
        # La priorité peut être calculée ici (par exemple, l'écart entre le seuil et la quantité)
        if produit.quantite < seuil_critique:
            # On inverse la priorité pour que le plus urgent (plus petit stock) soit en haut
            priorité = produit.quantite
            heapq.heappush(self.tas, (priorité, produit))
    
    def extraire(self):
        if self.tas:
            return heapq.heappop(self.tas)[1]
        return None

    def afficher_file(self):
        for item in self.tas:
            priorité, produit = item
            print(f"Priorité: {priorité} -> {produit}")
