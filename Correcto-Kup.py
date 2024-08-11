import tkinter as tk
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET
import os
from spellchecker import SpellChecker

class CorrectorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Correcto-Kup (French Only)")
        self.geometry("400x200")

        self.label = tk.Label(self, text="Sélectionnez un fichier .kup à corriger :")
        self.label.pack(pady=10)

        self.select_button = tk.Button(self, text="Sélectionner le fichier", command=self.select_file)
        self.select_button.pack(pady=10)

        self.file_path = ""
        self.spell = SpellChecker(language='fr')  # Initialiser l'outil de correction pour le français

    def select_file(self):
        self.file_path = filedialog.askopenfilename(
            filetypes=[("XML de Kuriimu", "*.kup"), ("Tous les fichiers", "*.*")]
        )
        if self.file_path:
            self.label.config(text=f"Fichier sélectionné : {os.path.basename(self.file_path)}")
            self.correct_button = tk.Button(self, text="Corriger et sauvegarder", command=self.correct_and_save)
            self.correct_button.pack(pady=10)

    def correct_french(self, text):
        words = text.split()
        corrected_words = [self.spell.candidates(word).pop() if self.spell.candidates(word) else word for word in words]
        corrected_text = ' '.join(corrected_words)
        return corrected_text

    def correct_xml_element(self, element):
        if element.text:
            element.text = self.correct_french(element.text)
        for subelement in element:
            self.correct_xml_element(subelement)

    def correct_and_save(self):
        try:
            tree = ET.parse(self.file_path)
            root = tree.getroot()
            self.correct_xml_element(root)

            output_file_path = filedialog.asksaveasfilename(
                defaultextension=".kup",
                filetypes=[("XML de Kuriimu", "*.kup"), ("Tous les fichiers", "*.*")]
            )
            if output_file_path:
                tree.write(output_file_path)
                messagebox.showinfo("Succès", f"KUP corrigé enregistré dans {output_file_path}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")

if __name__ == "__main__":
    app = CorrectorApp()
    app.mainloop()
