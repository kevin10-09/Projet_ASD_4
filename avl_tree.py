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

    def supprimer(self, id_produit):
        self.racine = self._supprimer_noeud(self.racine, id_produit)

    def _supprimer_noeud(self, node, id_produit):
        if not node:
            return node

        # Recherche du nœud à supprimer
        if id_produit < node.produit.id:
            node.gauche = self._supprimer_noeud(node.gauche, id_produit)
        elif id_produit > node.produit.id:
            node.droite = self._supprimer_noeud(node.droite, id_produit)
        else:
            # Nœud trouvé : suppression
            if not node.gauche:
                return node.droite
            elif not node.droite:
                return node.gauche
            else:
                # Cas où le nœud a deux enfants
                temp = self._trouver_min(node.droite)
                node.produit = temp.produit
                node.droite = self._supprimer_noeud(node.droite, temp.produit.id)

        # Mise à jour de la hauteur du nœud courant
        node.hauteur = 1 + max(self._hauteur(node.gauche), self._hauteur(node.droite))

        # Équilibrage du nœud
        balance = self._get_balance(node)

        # Cas de déséquilibre et rotations nécessaires
        # Rotation droite
        if balance > 1 and self._get_balance(node.gauche) >= 0:
            return self._rotation_droite(node)
        # Rotation gauche
        if balance < -1 and self._get_balance(node.droite) <= 0:
            return self._rotation_gauche(node)
        # Double rotation gauche-droite
        if balance > 1 and self._get_balance(node.gauche) < 0:
            node.gauche = self._rotation_gauche(node.gauche)
            return self._rotation_droite(node)
        # Double rotation droite-gauche
        if balance < -1 and self._get_balance(node.droite) > 0:
            node.droite = self._rotation_droite(node.droite)
            return self._rotation_gauche(node)

        return node

    def _trouver_min(self, node):
        # Trouver le nœud avec la valeur minimale dans un sous-arbre
        while node.gauche:
            node = node.gauche
        return node

    def mettre_a_jour(self, id_produit, nouveau_produit):
        # Supprimer l'ancien produit
        self.supprimer(id_produit)
        # Insérer le nouveau produit
        self.inserer(nouveau_produit)