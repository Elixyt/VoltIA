import pytesseract
from PIL import Image, ImageGrab
import tkinter as tk
from tkinter import messagebox
import asyncio
from sydney import SydneyClient
import os

# Définir l'endroit où se trouve l'exécutable Tesseract sur ton système
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ["BING_COOKIES"] = "<_C_Auth=; MC1=GUID=3100c6a11fc448d1bc84159cb2511551&HASH=3100&LV=202406&V=4&LU=1717264143654; MUID=2e1a7bf8f3ab402bbfd40e6ed1ede131; MS0=d0e3bf28d0634e31968c54fc7e7f24a1; _C_Auth=; MUIDB=2e1a7bf8f3ab402bbfd40e6ed1ede131; _EDGE_S=SID=0DC1FEC1466767F733E1EBDC4707667D; ak_bmsc=6D8FDF10336B6BE87DE7ED72969DC5CE~000000000000000000000000000000~YAAQGuzAF2ygwJeSAQAAeHwZpRlr/NweJ4p/6yJk6qKLEHOdttx9wyqBSHv6SXnbAVuXhROvt/yZE3cZczIg6ZzxYAIfFifjdkwKx/B3GPTOyw+MTSdRnxIRbkLEy1eGnYPGeeDV8CZQ/In7iKuZHJUFMS4KerG0HiegSauGv5P8W7HP9i4xBmdqghy+SdD3D1SdM71xlwdxFpNM90RPdE6pIwtxrdPRvB3nlc80RQB3MlHyTtZhshc91sC1N8lJuARw2Y68Qxyu+3YB5z0bUxpkNv89dHKMX/RwJVq5TRIybVwhdR3pSSetoAlwflI02xoUvDRxaDotY8xFz9Vcwvsdq226R2ZxlUmtXWNk0sEAkXGAVwGDGB6VN5TJvKPgC4Bpzwfcrx3ljR+d2g==; CMCCP=AD%3D1%26AL%3D1%26SM%3D1%26expires%3D1760882771531; BCP=AD%3D1%26AL%3D1%26SM%3D1%26expires%3D1760882771531; cl_dtrs=%5B%7B%22type%22%3A%22cl_dtrs%22%2C%22value%22%3A%22KZkDk7dQyMrucJ%5Cu002BTuoFOkXq7u8NNPEOPHs47rfxF8UY%5Cu002B%2FK5TPaDe1VZY%5Cu002B%5Cu002BQtl3UDxjJ%5Cu002Bbj1iCOM1Lc4EgcqylKml1XvNk7ioysme6xxeQP4suvnfXVqabd%2FsOz%5Cu002BFB9r5dPDdfjr1fqWQ40oarhPYl2tEkVq%5Cu002BkHgetMSF875okqYBK3tHX1zjNmB5%2F6MCIr9ZhmcLCg8BOAe4R5EuZM%2FG2%2FYY0MoMMiuppiQh3wjo%5Cu002Bn93sg59ozIvhy8gwb8tuh2F9aj2C1tXevBMSgGOMaYn6t%5Cu002BZCqMekmqUBYX48djpVLnC18UNZ9UfRQoY8YsZzJUrFxtD9odsl7Xw8yYm23%5Cu002ByQmYptxVi1ugZVyOCLAmqYS71ppuWpXGncMRB5IiguvELk6UBTnnXAh8iw9JTnsJF6IoY4Wt2v5bnpaNcVXgCWMA%3D%3AE1%22%7D%5D; bm_sv=AA9D9483614CB4283C5E6535DC5256CA~YAAQGuzAF30YwZeSAQAA/MwdpRm+n+ehWAK/W0c74KDECj/AtrRvLtPLHan2wGgJ6HAD+rjfYxbIVENPug1usnxv7jf+OL6G0gu16PDEXFwRJUG1uic7j+G7b1tlc0Cs3fK+zQQwPIewO8KEWKL9pWFpwRwgN8yfq+wWgnxRjonAi6Kkpmt9gf3zpjmjUewAB26TbfClqsj+rmKh5KqZusGN8txaEiMQ7ylpsbKjWPZ2UFRuBcta8jUM4WX+bFZqfmHIkA==~1>"
# Initialiser Sydney Client (GPT-4 via Bing Chat)
client = SydneyClient()  # Assure-toi de configurer correctement le token d'authentification Bing Chat si nécessaire

class ScreenCapture:
    def __init__(self):
        self.rect_start_x = None
        self.rect_start_y = None
        self.rect_end_x = None
        self.rect_end_y = None
        self.rect_id = None

        self.window = tk.Tk()
        self.window.attributes("-fullscreen", True)
        self.window.attributes("-alpha", 0.3)  # Fenêtre transparente
        self.canvas = tk.Canvas(self.window, cursor="cross", bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        # Commencer à dessiner le rectangle
        self.rect_start_x = event.x
        self.rect_start_y = event.y
        self.rect_id = self.canvas.create_rectangle(self.rect_start_x, self.rect_start_y, self.rect_start_x, self.rect_start_y, outline='red', width=2)

    def on_mouse_drag(self, event):
        # Ajuster le rectangle pendant que l'utilisateur déplace la souris
        self.rect_end_x, self.rect_end_y = (event.x, event.y)
        self.canvas.coords(self.rect_id, self.rect_start_x, self.rect_start_y, self.rect_end_x, self.rect_end_y)

    def on_button_release(self, event):
        # Finaliser le rectangle de sélection et capturer la zone
        self.rect_end_x = event.x
        self.rect_end_y = event.y
        self.window.quit()  # Fermer la fenêtre de sélection après la capture

    def get_bbox(self):
        # Assurer que les coordonnées sont bien ordonnées : (left, top, right, bottom)
        left = min(self.rect_start_x, self.rect_end_x)
        right = max(self.rect_start_x, self.rect_end_x)
        top = min(self.rect_start_y, self.rect_end_y)
        bottom = max(self.rect_start_y, self.rect_end_y)
        return (left, top, right, bottom)

def capture_rectangle():
    """Capture une zone rectangulaire de l'écran sélectionnée par l'utilisateur"""
    messagebox.showinfo("Sélection", "Sélectionnez une zone de l'écran avec votre souris.")
    
    # Créer une instance de la fenêtre de capture
    capture_tool = ScreenCapture()
    capture_tool.window.mainloop()

    # Obtenir les coordonnées de la zone sélectionnée
    bbox = capture_tool.get_bbox()
    
    # Capturer la capture d'écran de la zone sélectionnée
    screenshot = ImageGrab.grab(bbox)
    
    return screenshot

def extract_text(image):
    """Extraire le texte de l'image avec Tesseract"""
    text = pytesseract.image_to_string(image)
    return text

async def get_gpt4_response(question):
    """Utiliser Sydney.py pour générer une réponse via GPT-4"""
    response = await client.ask(question)
    return response

def on_button_click():
    """Action à effectuer lorsque le bouton est cliqué"""
    try:
        image = capture_rectangle()  # Capturer la zone sélectionnée
        text = extract_text(image)   # Extraire le texte de la capture

        # Afficher le texte capturé pour debug
        print(f"Texte capturé : {text}")
        
        if "?" in text:  # Vérifier s'il y a une question
            # Obtenir la réponse de GPT-4 via Sydney.py
            asyncio.run(async_process(text))
        else:
            answer_label.config(text="Pas de question détectée.")  # Indiquer qu'il n'y a pas de question
    except Exception as e:
        answer_label.config(text=f"Erreur : {str(e)}")

async def async_process(question):
    """Traitement asynchrone pour GPT-4 avec Sydney.py"""
    response = await get_gpt4_response(question)
    answer_label.config(text=response)  # Mettre à jour l'affichage avec la réponse
    capture_button.config(state=tk.DISABLED)  # Désactiver le bouton jusqu'à réinitialisation

def reset_application():
    """Réinitialiser l'application pour permettre une nouvelle capture"""
    answer_label.config(text="La réponse apparaîtra ici.")
    capture_button.config(state=tk.NORMAL)  # Réactiver le bouton de capture

# Configuration de la fenêtre principale de l'application
window = tk.Tk()
window.title("Assistant IA")

# Créer un bouton pour capturer une zone
capture_button = tk.Button(window, text="Capturer une zone", command=on_button_click)
capture_button.pack(pady=20)

# Créer un bouton pour réinitialiser l'application après la réponse
reset_button = tk.Button(window, text="Nouvelle question", command=reset_application)
reset_button.pack(pady=20)

# Créer une zone pour afficher la réponse
answer_label = tk.Label(window, text="La réponse apparaîtra ici.", wraplength=400, justify="left")
answer_label.pack(padx=20, pady=20)

# Démarrer la fenêtre principale
window.mainloop()
