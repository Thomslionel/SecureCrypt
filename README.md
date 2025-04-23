# SecureCrypt

## Description

SecureCrypt est une application de cryptographie conçue pour offrir des solutions sécurisées de chiffrement et de déchiffrement des données. Ce projet vise à protéger les informations sensibles en utilisant des algorithmes modernes et robustes.

## Sécurité

* Algorithme utilisé : AES-256 en mode CBC.
* Dérivation de clé : Utilisation de PBKDF2 avec 600 000 itérations pour dériver une clé à partir du mot de passe.
* Sel et IV : Générés aléatoirement pour chaque fichier et stockés dans le fichier chiffré.


## Limitation

* Si le mot de passe est incorrect ou si le fichier est corrompu, une erreur sera levée.
* L'application ne prend en charge que les fichiers individuels (pas de dossiers).

## Prérequis

- **Système d'exploitation** : Windows, macOS ou Linux.
- **Langage** : Python 3.x.
- **Bibliothèques nécessaires** :
    - `cryptography`
    - `pycryptodome`
    - Autres dépendances listées dans `requirements.txt`.

## Installation

1. Clonez le dépôt :
     ```bash
     git clone https://github.com/thomslionel/SecureCrypt.git
     cd SecureCrypt
     ```

2. Installez les dépendances :
     ```bash
     pip install -r requirements.txt
     ```

## Utilisation

1. Lancez l'application :
     ```bash
     python main.py
     ```

2. Lorsque vous lancez l'application, un écran de démarrage (splash screen) s'affiche pendant 3 secondes.

# Chiffrement
3. Cliquez sur le bouton "Chiffrer un fichier".
4. Sélectionnez un fichier à chiffrer.
5. Entrez un mot de passe robuste (minimum 8 caractères, avec chiffres, majuscules et caractères spéciaux).
Le fichier chiffré sera enregistré avec l'extension .enc.

# Dechiffrement
7. Cliquez sur le bouton "Déchiffrer un fichier".
8. Sélectionnez un fichier .enc à déchiffrer.
9. Entrez le mot de passe utilisé lors du chiffrement.
Le fichier déchiffré sera restauré avec son nom d'origine.

## Contribution

Les contributions sont les bienvenues ! Veuillez suivre les étapes suivantes :

1. Forkez le dépôt.
2. Créez une branche pour vos modifications :
     ```bash
     git checkout -b ma-branche
     ```
3. Effectuez vos changements et validez-les.
4. Soumettez une pull request.

## Licence

Ce projet est sous licence MIT. Consultez le fichier `LICENSE` pour plus d'informations.

## Auteurs

- **Nom de l'auteur** : Thomas MANLY
- **Contact** : thomsmanly@gmail.com

## Remerciements

Merci à toutes les personnes ayant contribué à ce projet et à la communauté open source pour leur soutien.
