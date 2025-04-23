# Import des packages
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256


class CryptoManager : 
    """
        Classe CryptoManager pour gérer le chiffrement et le déchiffrement des fichiers.
        Utilise AES-256 CBC et PBKDF2 pour dériver la clé.
    """

    # Définition du constructeur
    def __init__(self, pbkdf2_iterations: int = 600_000):
        self.pbkdf2_iterations = pbkdf2_iterations # Nombre d'iterations pour PBKDF2
        self.block_size = AES.block_size # Taille bloc pour AES (Généralement 16 octets)
    
    def derive_key(self, password: bytes, salt: bytes) -> bytes:
        """
        Dérive une clé AES-256 depuis un mot de passe et un sel via PBKDF2.
        """
        return PBKDF2(password, salt, dkLen=32, count=self.pbkdf2_iterations, hmac_hash_module=SHA256)
    

    def encrypt(self, filepath: str, password: str) -> str:
        """
        Chiffre le fichier au chemin donné avec le mot de passe et renvoie le chemin du fichier chiffré.
        """
        salt = get_random_bytes(16) # Génération du sel
        key = self.derive_key(password.encode(), salt) # Dérivation du password a partir du salt
        iv = get_random_bytes(16) # génération de IV
        cipher = AES.new(key, AES.MODE_CBC, iv) # Création d'un objet AES en mode CBC

        with open(filepath, 'rb') as f:
            plaintext = f.read() # Lecture du fichier a crypter en mode binaire

        # Configuration du Padding
        pad_len = self.block_size - len(plaintext) % self.block_size
        padding = bytes([pad_len] * pad_len)
        padded = plaintext + padding

        ciphertext = cipher.encrypt(padded) # chiffrement du texte
        out_path = filepath + '.enc' # chemin du fichier crypté

        with open(out_path, 'wb') as f_out:
            f_out.write(salt + iv + ciphertext) # Ecrit le salt, IV et le texte chiffré dans le fichier de sortie

        return out_path # Retourne le chemin du fichier crypté
    


    def decrypt(self, filepath: str, password: str) -> str:
        """
        Déchiffre le fichier .enc au chemin donné avec le mot de passe et renvoie le chemin du fichier déchiffré.
        """
        with open(filepath, 'rb') as f_in:
            data = f_in.read() # Lire le contenu du fichier à décrypter en mode binaire

        salt = data[:16] # Recupère le salt
        iv = data[16:32]# Recupère l'IV
        ciphertext = data[32:]# Recupère le texte chiffré
        key = self.derive_key(password.encode(), salt) # Dérive la clef a partir du mdp et du salt
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded = cipher.decrypt(ciphertext) # Dechiffre le texte chiffré

        # Remove PKCS7 padding
        pad_len = padded[-1]
        if pad_len < 1 or pad_len > self.block_size:
            raise ValueError("Mot de passe incorrect ou fichier corrompu.") # Verifie la validité du mdp
        plaintext = padded[:-pad_len] # Recupère le padding

        out_path = filepath[:-4]  
        with open(out_path, 'wb') as f_out:
            f_out.write(plaintext) # Ecrit le texte en clair dans le fichier

        return out_path # Retourne le chemin du fichier déchiffré