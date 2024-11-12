import tkinter as tk
from tkinter import scrolledtext, END
import string
import os
import json
import urllib.request

# URL der Wortliste
WORDLIST_URL = "https://raw.githubusercontent.com/Jonny-exe/German-Words-Library/refs/heads/master/German-words-1600000-words-multilines.json"
LOCAL_WORDLIST_FILE = "german_words.json"

class CaesarCipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Caesar-Verschlüsselung Entschlüsseln")
        self.root.geometry("600x400")
        
        # Create GUI components
        self.create_widgets()
        
        # Download wordlist if necessary
        self.download_wordlist()
        
    def create_widgets(self):
        # Eingabefeld für die verschlüsselte Nachricht
        input_label = tk.Label(self.root, text="Verschlüsselte Nachricht:")
        input_label.pack(pady=5)
        self.input_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=70, height=5)
        self.input_text.pack(pady=5)

        # Button zum Entschlüsseln
        decrypt_button = tk.Button(self.root, text="Entschlüsseln", command=self.decrypt_message)
        decrypt_button.pack(pady=5)

        # Read-only Ausgabe Textfeld für die entschlüsselte Nachricht
        output_label = tk.Label(self.root, text="Entschlüsselte Nachricht:")
        output_label.pack(pady=5)
        self.output_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=70, height=5)
        self.output_text.pack(pady=5)
        self.output_text.config(state=tk.DISABLED)

        # Listbox für die besten Verschiebungen
        shift_label = tk.Label(self.root, text="Beste Verschiebungen:")
        shift_label.pack(pady=5)
        self.shift_list = tk.Listbox(self.root, height=10, width=70)
        self.shift_list.pack(pady=5)

        # Bind event to handle click on the listbox
        self.shift_list.bind("<<ListboxSelect>>", self.load_shifted_message)
    
    def download_wordlist(self):
        if not os.path.exists(LOCAL_WORDLIST_FILE):
            print("Wortliste wird heruntergeladen...")
            urllib.request.urlretrieve(WORDLIST_URL, LOCAL_WORDLIST_FILE)
            print("Wortliste erfolgreich heruntergeladen.")
        else:
            print("Wortliste bereits vorhanden.")
    
    # Caesar Entschlüsselung
    def caesar_decrypt(self, ciphertext, shift):
        decrypted_text = []
        for char in ciphertext:
            if char in string.ascii_lowercase:
                index = (string.ascii_lowercase.index(char) - shift) % 26
                decrypted_text.append(string.ascii_lowercase[index])
            elif char in string.ascii_uppercase:
                index = (string.ascii_uppercase.index(char) - shift) % 26
                decrypted_text.append(string.ascii_uppercase[index])
            else:
                decrypted_text.append(char)
        return ''.join(decrypted_text)
    
    # Bestimmung der besten Verschiebung durch Vergleich mit der Wortliste
    def caesar_break(self, ciphertext):
        # Lade die Wortliste
        with open(LOCAL_WORDLIST_FILE, "r", encoding="utf-8") as f:
            common_words = set(word.lower() for word in json.load(f))

        shifts = []

        # Probiere alle möglichen Verschiebungen (1 bis 25)
        for shift in range(1, 26):
            decrypted_text = self.caesar_decrypt(ciphertext, shift)
            words = decrypted_text.lower().split()
            matches = sum(1 for word in words if word in common_words)
            shifts.append((shift, decrypted_text, matches))

        shifts.sort(key=lambda x: (-x[2], x[0]))
        return shifts
    
    # Funktion, die bei Klick auf den Button ausgeführt wird
    def decrypt_message(self):
        ciphertext = self.input_text.get("1.0", END).strip()
        self.shifts = self.caesar_break(ciphertext)

        # Update output text with the best decrypted message
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, END)
        self.output_text.insert(END, self.shifts[0][1])
        self.output_text.config(state=tk.DISABLED)

        # Update listbox with shifts
        self.shift_list.delete(0, END)
        for i, (shift, decrypted, matches) in enumerate(self.shifts):
            display_text = f"Shift {shift}: {decrypted[:50]}... ({matches} valid words)"
            self.shift_list.insert(END, display_text)
            if i == 0:
                self.shift_list.itemconfig(0, {'bg': 'lightgreen'})
    
    # Load the shifted message when an item is clicked in the listbox
    def load_shifted_message(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            _, decrypted, _ = self.shifts[index]
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete(1.0, END)
            self.output_text.insert(END, decrypted)
            self.output_text.config(state=tk.DISABLED)

# Starte das GUI-Hauptfenster
root = tk.Tk()
app = CaesarCipherApp(root)
root.mainloop()