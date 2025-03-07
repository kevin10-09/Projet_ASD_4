import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import re  # Pour la validation de la date

# Importations des classes personnalisées
from dynamic_array import DynamicArray
from avl_tree import AVLTree
from priority_queue import PriorityQueue
from models import Produit

class GestionStockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire Intelligent de Stocks")
        self.root.geometry("1000x600")  # Taille de la fenêtre
        self.root.configure(bg="#f0f0f0")  # Couleur de fond

        # Initialisation des structures de données
        self.stock = DynamicArray()
        self.arbre = AVLTree()
        self.file_prioritaire = PriorityQueue()
        self.seuil_critique = 5  # Seuil critique pour la file de priorité

        # Configuration des styles
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 12))
        self.style.configure("TButton", font=("Helvetica", 12), padding=10)
        self.style.configure("Header.TLabel", font=("Helvetica", 16, "bold"))

        # Création de l'interface
        self.creer_interface()

    def creer_interface(self):
        # Cadre principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Titre
        ttk.Label(main_frame, text="Gestion des Stocks", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=10)

        # Formulaire de saisie
        form_frame = ttk.Frame(main_frame)
        form_frame.grid(row=1, column=0, sticky=tk.W, pady=10)

        ttk.Label(form_frame, text="ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.id_entry = ttk.Entry(form_frame, width=30)
        self.id_entry.grid(row=0, column=1, pady=5)

        ttk.Label(form_frame, text="Nom:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.nom_entry = ttk.Entry(form_frame, width=30)
        self.nom_entry.grid(row=1, column=1, pady=5)

        ttk.Label(form_frame, text="Quantité:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.quantite_entry = ttk.Entry(form_frame, width=30)
        self.quantite_entry.grid(row=2, column=1, pady=5)

        ttk.Label(form_frame, text="Prix:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.prix_entry = ttk.Entry(form_frame, width=30)
        self.prix_entry.grid(row=3, column=1, pady=5)

        ttk.Label(form_frame, text="Date d'expiration (YYYY-MM-DD):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.date_entry = ttk.Entry(form_frame, width=30)
        self.date_entry.grid(row=4, column=1, pady=5)

        # Boutons
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=2, column=0, pady=20)

        ttk.Button(buttons_frame, text="Ajouter", command=self.ajouter_produit).grid(row=0, column=0, padx=5)
        ttk.Button(buttons_frame, text="Modifier", command=self.modifier_produit).grid(row=0, column=1, padx=5)
        ttk.Button(buttons_frame, text="Supprimer", command=self.supprimer_produit).grid(row=0, column=2, padx=5)
        ttk.Button(buttons_frame, text="Rechercher", command=self.rechercher_produit).grid(row=0, column=4, padx=5)
        ttk.Button(buttons_frame, text="File Prioritaire", command=self.afficher_file_prioritaire).grid(row=0, column=5, padx=5)

        # Tableau pour afficher les produits
        self.tree = ttk.Treeview(main_frame, columns=("ID", "Nom", "Quantité", "Prix", "Date d'expiration"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nom", text="Nom")
        self.tree.heading("Quantité", text="Quantité")
        self.tree.heading("Prix", text="Prix")
        self.tree.heading("Date d'expiration", text="Date d'expiration")
        self.tree.grid(row=3, column=0, columnspan=2, pady=20, sticky=tk.W+tk.E)

        # Barre de statut
        self.status_var = tk.StringVar()
        self.status_var.set("Prêt")
        ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W).grid(row=4, column=0, sticky=tk.W+tk.E, pady=10)

    def ajouter_produit(self):
        try:
            # Récupérer les données du formulaire
            id_produit = self.id_entry.get().strip()
            nom = self.nom_entry.get().strip()
            quantite = int(self.quantite_entry.get().strip())
            prix = float(self.prix_entry.get().strip())
            date_exp = self.date_entry.get().strip()

            # Validation de la date
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_exp):
                messagebox.showerror("Erreur", "Format de date invalide. Utilisez 'YYYY-MM-DD'.")
                return

            try:
                datetime.strptime(date_exp, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Erreur", "Date invalide. Vérifiez la date.")
                return

            # Créer le produit
            produit = Produit(id_produit, nom, quantite, prix, date_exp)

            # Ajouter le produit au stock, à l'arbre AVL et à la file de priorité
            self.stock.ajouter_produit(produit)
            self.arbre.inserer(produit)
            self.file_prioritaire.ajouter(produit, self.seuil_critique)

            # Mettre à jour le tableau
            self.afficher_produits()

            # Réinitialiser les champs du formulaire
            self.id_entry.delete(0, tk.END)
            self.nom_entry.delete(0, tk.END)
            self.quantite_entry.delete(0, tk.END)
            self.prix_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)

            # Afficher un message de succès
            self.status_var.set("Produit ajouté avec succès!")
            messagebox.showinfo("Succès", "Produit ajouté avec succès!")
        except ValueError as e:
            self.status_var.set(f"Erreur: {str(e)}")
            messagebox.showerror("Erreur", str(e))
        except Exception as e:
            self.status_var.set(f"Une erreur inattendue s'est produite: {str(e)}")
            messagebox.showerror("Erreur", str(e))

    def afficher_produits(self):
        # Effacer le tableau actuel
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Ajouter les produits dans le tableau
        for produit in self.stock.array:
            self.tree.insert("", tk.END, values=(
                produit.id,
                produit.nom,
                produit.quantite,
                f"{produit.prix:.2f}",  # Formatage du prix avec 2 décimales
                produit.date_expiration.strftime("%Y-%m-%d")
            ))

        # Ajuster les colonnes pour qu'elles s'adaptent au contenu
        for col in self.tree["columns"]:
            self.tree.column(col, width=100, anchor=tk.CENTER)
            self.tree.heading(col, text=col, anchor=tk.CENTER)

        self.status_var.set("Liste des produits mise à jour.")

    def modifier_produit(self):
        try:
            id_produit = self.id_entry.get().strip()
            nouvelle_quantite = int(self.quantite_entry.get().strip())

            # Modifier la quantité dans le stock
            self.stock.modifier_produit(id_produit, quantite=nouvelle_quantite)
            # Mise à jour dans la file de priorité
            produit = self.arbre.rechercher(id_produit)
            if produit:
                self.file_prioritaire.ajouter(produit, self.seuil_critique)

            # Mettre à jour le tableau
            self.afficher_produits()
            # Réinitialiser les champs du formulaire
            self.id_entry.delete(0, tk.END)
            self.nom_entry.delete(0, tk.END)
            self.quantite_entry.delete(0, tk.END)
            self.prix_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)

            self.status_var.set("Produit modifié avec succès!")
            messagebox.showinfo("Succès", "Produit modifié avec succès!")
        except ValueError as e:
            self.status_var.set(f"Erreur: {str(e)}")
            messagebox.showerror("Erreur", str(e))
        except Exception as e:
            self.status_var.set(f"Une erreur inattendue s'est produite: {str(e)}")
            messagebox.showerror("Erreur", str(e))

    def supprimer_produit(self):
        try:
            id_produit = self.id_entry.get().strip()

            # Supprimer le produit du stock
            self.stock.supprimer_produit(id_produit)

            # Supprimer le produit de l'arbre AVL
            self.arbre.supprimer(id_produit)

            # Supprimer le produit de la file de priorité
            #self.file_prioritaire.supprimer(id_produit)

            # Mettre à jour le tableau
            self.afficher_produits()
             # Réinitialiser les champs du formulaire
            self.id_entry.delete(0, tk.END)
            self.nom_entry.delete(0, tk.END)
            self.quantite_entry.delete(0, tk.END)
            self.prix_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)

            self.status_var.set("Produit supprimé avec succès!")
            messagebox.showinfo("Succès", "Produit supprimé avec succès!")
        except ValueError as e:
            self.status_var.set(f"Erreur: {str(e)}")
            messagebox.showerror("Erreur", str(e))
        except Exception as e:
            self.status_var.set(f"Une erreur inattendue s'est produite: {str(e)}")
            messagebox.showerror("Erreur", str(e))

    def rechercher_produit(self):
        try:
            id_produit = self.id_entry.get().strip()

            # Vérifier si l'ID est vide
            if not id_produit:
                messagebox.showwarning("Avertissement", "Veuillez entrer un ID pour la recherche.")
                return

            # Rechercher le produit dans l'arbre AVL
            produit = self.arbre.rechercher(id_produit)
            # Réinitialiser les champs du formulaire
            self.id_entry.delete(0, tk.END)
            self.nom_entry.delete(0, tk.END)
            self.quantite_entry.delete(0, tk.END)
            self.prix_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)


            if produit:
                messagebox.showinfo("Résultat", str(produit))
                self.status_var.set(f"Produit trouvé: {produit.nom}")
            else:
                messagebox.showinfo("Résultat", "Produit non trouvé.")
                self.status_var.set("Produit non trouvé.")
        except Exception as e:
            self.status_var.set(f"Erreur lors de la recherche du produit: {str(e)}")
            messagebox.showerror("Erreur", str(e))

    def afficher_file_prioritaire(self):
        try:
            file_content = self.file_prioritaire.afficher_file()
            messagebox.showinfo("File Prioritaire", file_content)
            self.status_var.set("File prioritaire affichée.")
        except Exception as e:
            self.status_var.set(f"Erreur lors de l'affichage de la file prioritaire: {str(e)}")
            messagebox.showerror("Erreur", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = GestionStockApp(root)
    root.mainloop()