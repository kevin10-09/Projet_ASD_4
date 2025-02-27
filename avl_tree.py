# avl_tree.py
class AVLNode:
    def __init__(self, produit):
        self.produit = produit
        self.gauche = None
        self.droite = None
        self.hauteur = 1

class AVLTree:
    def __init__(self):
        self.racine = None

    def _hauteur(self, node):
        if not node:
            return 0
        return node.hauteur

    def _rotation_droite(self, y):
        x = y.gauche
        T2 = x.droite
        
        # Rotation
        x.droite = y
        y.gauche = T2
        
        # Mise à jour des hauteurs
        y.hauteur = 1 + max(self._hauteur(y.gauche), self._hauteur(y.droite))
        x.hauteur = 1 + max(self._hauteur(x.gauche), self._hauteur(x.droite))
        return x

    def _rotation_gauche(self, x):
        y = x.droite
        T2 = y.gauche
        
        # Rotation
        y.gauche = x
        x.droite = T2
        
        # Mise à jour des hauteurs
        x.hauteur = 1 + max(self._hauteur(x.gauche), self._hauteur(x.droite))
        y.hauteur = 1 + max(self._hauteur(y.gauche), self._hauteur(y.droite))
        return y

    def _get_balance(self, node):
        if not node:
            return 0
        return self._hauteur(node.gauche) - self._hauteur(node.droite)

    def inserer(self, produit):
        self.racine = self._inserer_noeud(self.racine, produit)

    def _inserer_noeud(self, node, produit):
        if not node:
            return AVLNode(produit)
        # Ici, on peut choisir de comparer par identifiant ou par nom
        if produit.id < node.produit.id:
            node.gauche = self._inserer_noeud(node.gauche, produit)
        else:
            node.droite = self._inserer_noeud(node.droite, produit)

        node.hauteur = 1 + max(self._hauteur(node.gauche), self._hauteur(node.droite))
        balance = self._get_balance(node)

        # Cas de déséquilibre et rotations nécessaires
        # Rotation droite
        if balance > 1 and produit.id < node.gauche.produit.id:
            return self._rotation_droite(node)
        # Rotation gauche
        if balance < -1 and produit.id > node.droite.produit.id:
            return self._rotation_gauche(node)
        # Double rotation gauche-droite
        if balance > 1 and produit.id > node.gauche.produit.id:
            node.gauche = self._rotation_gauche(node.gauche)
            return self._rotation_droite(node)
        # Double rotation droite-gauche
        if balance < -1 and produit.id < node.droite.produit.id:
            node.droite = self._rotation_droite(node.droite)
            return self._rotation_gauche(node)

        return node

    def rechercher(self, id_produit):
        return self._rechercher_noeud(self.racine, id_produit)

    def _rechercher_noeud(self, node, id_produit):
        if not node:
            return None
        if node.produit.id == id_produit:
            return node.produit
        elif id_produit < node.produit.id:
            return self._rechercher_noeud(node.gauche, id_produit)
        else:
            return self._rechercher_noeud(node.droite, id_produit)

    # Les méthodes de mise à jour et de suppression suivront une logique similaire en veillant à rééquilibrer l'arbre.
