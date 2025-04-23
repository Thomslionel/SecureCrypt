# Import des packages
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
from cryptoManager import CryptoManager
import re

class InterfaceUser:
    def __init__(self, master):
        self.master = master # Définition de la fenêtre principale
        master.title("SecureCrypt") # Titre de la fenêtre
        master.geometry("680x500") # Dimensions
        master.configure(bg="#2E3440") # Couleur de fonf
        master.resizable(False, False) # Impossible de le redimensionner

        # Configuration du style
        self._configure_styles()
        self.backend = CryptoManager() # Création de l'objet CryptoManager

        # Création des composants
        self._create_widgets()

    def _configure_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Palette de couleurs 
        self.colors = {
            "background": "#2E3440",
            "primary": "#5E81AC",
            "secondary": "#81A1C1",
            "text": "#ECEFF4",
            "error": "#BF616A",
            "success": "#A3BE8C"
        }

        # Configuration des styles
        self.style.configure("TFrame", background=self.colors["background"])
        self.style.configure("TLabel", 
                           background=self.colors["background"], 
                           foreground=self.colors["text"])
        self.style.configure("TButton", 
                           font=("Roboto", 10),
                           padding=10,
                           background=self.colors["primary"],
                           foreground=self.colors["text"])
        self.style.map("TButton",
                      background=[("active", self.colors["secondary"])])

    def _create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.master)
        main_frame.pack(pady=30, padx=30, fill="both", expand=True)

        # En-tête
        header = ttk.Label(main_frame, 
                          text="🔐 SecureCrypt", 
                          font=("Segoe UI", 18, "bold"), 
                          foreground="#88C0D0")
        header.pack(pady=(0, 20))

        # Icône dynamique
        self.icon_label = ttk.Label(main_frame, 
                                   text="🔒", 
                                   font=("Segoe UI", 48),
                                   foreground=self.colors["primary"])
        self.icon_label.pack(pady=10)

        # Champ mot de passe
        pw_frame = ttk.Frame(main_frame)
        pw_frame.pack(pady=15)
        
        ttk.Label(pw_frame, text="Mot de passe:").grid(row=0, column=0, padx=5)
        self.pw_var = tk.StringVar()
        self.pw_entry = ttk.Entry(pw_frame, 
                                 textvariable=self.pw_var, 
                                 show="*", 
                                 width=30,
                                 font=("Roboto", 10))
        self.pw_entry.grid(row=0, column=1)
        self.pw_entry.bind("<KeyRelease>", self._update_password_strength)

        # Indicateur de force
        self.strength_bar = ttk.Progressbar(main_frame, 
                                           orient="horizontal",
                                           length=200,
                                           mode="determinate")
        self.strength_bar.pack(pady=5)

        # Boutons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        self.encrypt_btn = ttk.Button(btn_frame, 
                                     text="Chiffrer un fichier", 
                                     command=self.encrypt_file)
        self.encrypt_btn.pack(side="left", padx=10)
        
        self.decrypt_btn = ttk.Button(btn_frame, 
                                     text="Déchiffrer un fichier", 
                                     command=self.decrypt_file)
        self.decrypt_btn.pack(side="left", padx=10)

        # Barre de statut
        self.status_var = tk.StringVar(value="Prêt à chiffrer/déchiffrer")
        status_bar = ttk.Label(self.master, 
                             textvariable=self.status_var,
                             relief="sunken",
                             anchor="center",
                             font=("Roboto", 9),
                             foreground=self.colors["text"],
                             background="#3B4252")
        status_bar.pack(side="bottom", fill="x")

    def _update_password_strength(self, event):
        """
        Utiliser pour évaluer la robustesse du mot de passe saisi par l'utilisateur en temps réel et afficher visuellement sa force à l'aide d'une barre de progression.

        Args:
            event (_type_): _description_
        """
        password = self.pw_var.get()
        strength = 0
        
        # Vérifie la robustesse tu mdp
        if len(password) >= 8: strength += 25
        if re.search(r"\d", password): strength += 25
        if re.search(r"[A-Z]", password): strength += 25
        if re.search(r"[!@#$%^&*]", password): strength += 25
        
        self.strength_bar["value"] = strength # Met à jour la barre de progression
        self.strength_bar["style"] = "danger.Horizontal.TProgressbar" if strength < 50 else "success.Horizontal.TProgressbar" if strength == 100 else "warning.Horizontal.TProgressbar"

    def encrypt_file(self):
        """
             Fonction qui, a partir du mdp fournit, et du filepath du fichier,  crypté le fichier.

        Returns:
            _type_: _description_
        """
        filepath = filedialog.askopenfilename() # Ouverture d'une boite de dialogue pour selectionner le fichier a chiffrer
        if not filepath:
            return
        
        password = self.pw_var.get() # Recupère le mdp saisi par le user
        if not self._validate_password(password): 
            return # valide le mdp

        try:
            self.status_var.set("Chiffrement en cours...") # Met à jour la barre de statut
            self.master.update()
            
            output_path = self.backend.encrypt(filepath, password) # Chiffre le fichier
            
            # Met a jour le statut et affiche un messagebox
            self.status_var.set("Chiffrement réussi!")
            messagebox.showinfo("Succès", f"Fichier chiffré:\n{output_path}")
            self.icon_label.config(text="🔓")
            
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
        finally:
            self.status_var.set("Prêt à chiffrer/déchiffrer")

    def decrypt_file(self):
        """
        Fonction qui, a partir du mdp fournit, et du filepath du fichier crypté, décrypte le fichier.
        """
        filepath = filedialog.askopenfilename (filetypes=[("Fichiers chiffrés", "*.enc")]) # Ouverture d'une boite de dialogue pour selectionner le fichier a déchiffrer
        if not filepath:
            return

        password = self.pw_var.get() # Recupère le mdp
        if not password:
            messagebox.showerror("Erreur", "Veuillez entrer le mot de passe")
            return

        try:
            self.status_var.set("Déchiffrement en cours...")
            self.master.update() # Met a jour le statut
            
            output_path = self.backend.decrypt(filepath, password) # Decrypter le fichier
            
             # Met a jour le statut et affiche un messagebox
            self.status_var.set("Déchiffrement réussi!")
            messagebox.showinfo("Succès", f"Fichier déchiffré:\n{output_path}")
            self.icon_label.config(text="🔒")
            
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
        finally:
            self.status_var.set("Prêt à chiffrer/déchiffrer")

    def _validate_password(self, password):
        """
           Vérifier que le mot de passe respecte les critères de sécurité
        Args:
            password (_type_): _description_

        Returns:
            _type_: _description_
        """
        if len(password) < 8:
            messagebox.showerror("Erreur", "Le mot de passe doit contenir au moins 8 caractères")
            return False
        if not re.search(r"\d", password):
            messagebox.showerror("Erreur", "Le mot de passe doit contenir un chiffre")
            return False
        if not re.search(r"[A-Z]", password):
            messagebox.showerror("Erreur", "Le mot de passe doit contenir une majuscule")
            return False
        if not re.search(r"[!@#$%^&*]", password):
            messagebox.showerror("Erreur", "Le mot de passe doit contenir un caractère spécial")
            return False
        return True