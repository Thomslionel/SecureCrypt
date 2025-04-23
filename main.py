from tkinter import Tk, Label
from PIL import Image, ImageTk
import os
from pathlib import Path
from interfaceUser import InterfaceUser

# --- Splash Screen ---
# splash_root = Tk()
# splash_root.overrideredirect(True)
# splash_root.geometry("400x300")
# splash_root.eval("tk::PlaceWindow . center")
# splash_root.configure(bg="white")

# try:
#     current_dir = Path(__file__).parent
#     image_path = current_dir / "image" / "splash.png"
    
#     if not image_path.exists():
#         raise FileNotFoundError(f"Fichier introuvable : {image_path}")
    
#     # Chargement et redimensionnement de l’image
#     original_image = Image.open(image_path)
#     resized_image = original_image.resize((400, 300), Image.Resampling.LANCZOS)
#     splash_image = ImageTk.PhotoImage(resized_image)
    
#     img_label = Label(splash_root, image=splash_image, bg="white")
#     img_label.image = splash_image  # Conserver la référence
#     img_label.pack(expand=True)

# except Exception as e:
#     error_text = f"Erreur de chargement : {str(e)}\n"
#     error_text += f"Chemin essayé : {image_path}"
#     Label(splash_root, 
#          text=error_text, 
#          bg="white", 
#          fg="red", 
#          font=("Arial", 10),
#          wraplength=380).pack(expand=True)

# splash_root.after(3000, splash_root.destroy)
# splash_root.mainloop()



if __name__ == "__main__":
    root = Tk() # Création d'un objet de Tkinter
    app = InterfaceUser(root) # Création d'un objet de la classe InterfaceUser
    root.eval("tk::PlaceWindow . center") # Garanti que la fenêtre s'ouvrira au centre de l'ecran
    root.mainloop() # Démarre l'application
