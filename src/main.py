print("Importing...")
from ascii_art import get_hangmans
import urllib.request
import os
import json
import random
import string
import sys
from getpass import getpass # getpass wird benutzt um das geheime Wort während der Eingabe nicht zu zeigen 

print("Imported!")

class HangmanGame:
    def __init__(self) -> None:
        # Variablen auf Standardwert initialisieren
        self.set_variables()
        self.clear_console()
        
        self.hangmans = get_hangmans()
        
        self.wordlist_link = "https://raw.githubusercontent.com/Jonny-exe/German-Words-Library/refs/heads/master/German-words-1600000-words-multilines.json"
        self.wordlist_path = "german_words.json"
        
        # Wortliste vorbereiten
        self.download_wordlist()
        self.prepare_wordlist()
        
    def set_variables(self) -> None:
        """Variablen auf ihren Standardwert setzten
        """
        
        self.lives_remaining_default: int = 6 # Standardanzahl der Leben
        self.lives_remaining: int = self.lives_remaining_default # Aktuelle Lebensanzahl des Spielers
        self.easy_mode: bool = None # Aktiviert / Deaktiviert den einfachen Spielmodus
        self.game_running: bool = None # Gibt an, ob das Spiel aktuell läuft
        self.secret_word_upper: str = None # Geheimes wort in Großbuchstaben (für die Ausgabe zum Benutzer)
        self.secret_word_lower: str = None # Geheimes Wort in Kleinbuchstaben (zum Vergleichen mit der wordlist)
        self.revealed_word: str = None # Aktuell aufgedecktes Wort als String (wird benutzt, um das Spiel zu beenden, wenn das ganze Wort aufgedeckt wurde)
        self.guessed_letters: list = [] # Liste an bereits erratenen Buchstaben
        self.wrong_letters: list = [] # Liste mit allen falsch geratenen Buchstaben
        self.right_letters: list = [] # Liste mit allen richtig geratenen Buchstaben
        self.wordlist_content: list = None # Liste an Wörten, die in der wordlist stehen
        
    def start_game(self) -> None:
        """Funktion, um das Spiel zu starten
        """
        
        self.clear_console()
        # Unendlicher while-loop, sodass man mehrere Runden hintereinander spielen kann
        while True:
            # Spielenstellungen vom Benutzer bekommen
            self.get_game_settings()
            self.game_running = True
            
            # Solange das aktuell Spiel läuft
            while self.game_running: 
                # "Benutzeroberfläche ausgeben"
                self.print_gui()
                
                # Eingabe vom Benutzer bekommen und verarbeiten
                user_input = self.get_user_input()
                right_input = self.process_user_input(user_input)
                
                # Bei falscher Eingabe ein Leben abziehen
                if not right_input:
                    self.lives_remaining -= 1
                
                # Wenn keine Leben mehr vorhanden sind das Spiel beenden
                if self.lives_remaining == 0:
                    self.game_finished(won=False)
                
                # Wortausgabe aktualisieren und wenn das ganze Wort aufgedeckt wurde das Spiel beenden
                self.generate_word_output()
                if self.revealed_word == self.secret_word_lower:
                    self.game_finished(won=True)
                
    def get_game_settings(self) -> None:
        """Geheimes Wort und den "Spielmodus" vom Benutzer bekommen
        """
        
        # Variablen zurücksetzen, falls sie bereits beschrieben wurden
        self.set_variables()
        
        # Usereingabe für das geheime Wort bekommen und überprüfen, ob es ein valides deutsches Wort ist
        self.clear_console()
        self.get_secret_word()
        self.clear_console()
        
        # Usereingabe für den "Spielmodus" bekommen
        self.ask_game_mode()
    
    def process_user_input(self, user_input: str):
        """_summary_

        Args:
            user_input (str): Benutzereingabe, die verarbeitet werden soll

        Returns:
            bool: Hat der Spieler einen richtigen Buchstaben geraten?
            bool: Hat der Spieler das ganze Wort erraten?
        """
        
        # Benutzereingabe vorbereiten
        user_input_upper = user_input.upper().strip()
        
        # Unterscheidung zwischen einzelnem Buchstaben und ganzem Wort
        if len(user_input) != 1:
            # Hat der Spieler das ganze Wort richtig geraten?
            if user_input_upper == self.secret_word_upper:
                self.game_finished(won=True) # Wenn das ganze Wort richtig geraten wurde, wird das Spiel direkt beendet.
                return True
            else:
                return False
            
        else:
            self.guessed_letters.append(user_input_upper) # An die Liste der geratenen Buchstaben anhängen
            
            # Wenn der einfache Modus aktiviert ist und der Spieler einen Buchstaben versucht, der bereits versucht wurde, verliert er kein Leben
            if (user_input_upper in self.right_letters or user_input_upper in self.wrong_letters) and self.easy_mode:
                return True
            # Sonst Unterscheidung, ob der Buchstabe richtig war und Anhängen an das zugehörige Array
            elif user_input_upper in self.secret_word_upper:
                self.right_letters.append(user_input_upper) # An die Liste der richtig geratenen Buchstaben anhängen
                return True
            else:
                self.wrong_letters.append(user_input_upper) # An die Liste der falsch geratenen Buchstaben anhängen
                return False
        
    def print_gui(self) -> None:
        """"Benutzeroberfläche" ausgeben
        """
        
        self.clear_console()
        
        # Hangman ausgeben, der zu den aktuellen Leben passt
        print(self.hangmans[self.lives_remaining_default - self.lives_remaining])
        
        # Wort ausgeben, das Unterstriche als Lücken für noch nicht erratene Buchstaben hat
        word_output = self.generate_word_output()
        
        print(" ".join(word_output))
        
        if self.easy_mode:
            print("Noch zu ratene Buchstaben: ", end="")
            for letter in string.ascii_uppercase:
                if letter not in set(self.guessed_letters):
                    print(f"{letter.upper()} ", end="")
            
            print("\n")
            
    def clear_console(self) -> None:
        """Konsole leeren
        """
        
        os.system("cls" if os.name == "nt" else "clear")
    
    def generate_word_output(self) -> list:
        """Generiert eine Liste mit Buchstaben für erratene Buchstaben und Unterstriche für noch nicht erratene Buchstaben

        Returns:
            list: Liste mit Buchstaben und Unterstrichen
        """
        
        self.revealed_word = ""
        
        # Liste mit der richtigen Länge an Unterstrichen erstellen
        word_output = ["_"] * len(self.secret_word_upper)
        
        # Set erstellen, um Duplikate zu entfernen und die Speichereffizenz zu verbessern
        right_letters_set = set(self.right_letters)
        
        # Alle Buchstaben durchgehen und bei einem bereits erratenen Buchstaben den Unterstrich durch den Buchstaben ersetzen
        for i, letter in enumerate(self.secret_word_upper):
            if letter in right_letters_set:
                word_output[i] = letter
                self.revealed_word += letter
                
        # Alles in Kleinbuchstaben umwandeln
        self.revealed_word = self.revealed_word.lower()
                    
        return word_output
    
    ########################################################################################
    
    def download_wordlist(self):
        """Lädt die Wortliste herunter, falls sie noch nicht vorhanden ist
        """
        
        print("Status der Wortliste überprüfen...")
        # Überprüft, ob die Datei noch nicht existiert
        if not os.path.exists(self.wordlist_path):
            print("Wortliste wird heruntergeladen...")
            # Lädt die Wortliste auf den angegebenen Pfad herunter
            urllib.request.urlretrieve(self.wordlist_link, self.wordlist_path)
            print("Wortliste erfolgreich heruntergeladen.")
        else:
            print("Wortliste bereits vorhanden.")
            
    def prepare_wordlist(self):
        """Lädt die Wortliste in die Variable self.wordlist_content
        """
        
        print("Loading Wordlist...")
        # Öffnet die Wortliste, liest den Inhalt im JSON Format Wort für Wort aus und wandelt Sonderzeichen um
        with open(self.wordlist_path, "r", encoding="utf-8") as f:
            common_words = list(self.convert_word_to_standard_characters(word.lower()) for word in json.load(f))
        print("Wordlist loaded")
            
        self.wordlist_content = common_words # Wörter in der Variable speichern
            
    def ask_game_mode(self):
        """Fragt den Benutzer nach dem zu verwendenden Spielmodus
        """
        
        # Usereingabe für die Einstellung des Easy-Modes und überprüfen, ob die Eingabe valide ist
        while self.easy_mode == None:
            # easy_mode_input = input("Möchtest du den einfachen Modus aktivieren? (Y/N): ")
            try:
                easy_mode_input = input("Möchtest du den einfachen Modus aktivieren? (Y / N, Enter / Q zum Schließen): ").lower()
            except (EOFError, KeyboardInterrupt):
                self.close()
            
            # Verarbeitung der Eingabe und Speichern des Modus
            if easy_mode_input == "y":
                self.easy_mode = True
            elif easy_mode_input == "n" or easy_mode_input == "":
                self.easy_mode = False
            elif easy_mode_input == "q":
                self.close()
            else:
                print("Ungültige Eingabe! - mögliche Eingaben: Y - N")
                
    def get_secret_word(self):
        """Geheimes Wort vom Benutzer bekommen und überprüfen, ob es ein valides deutsches Wort ist
        """
        
        # Wiederhole bis der Benutzer ein valides Wort eingegeben hat
        while self.secret_word_upper == None:
            # Benutzereingabe mit "getpass" anstatt "input", sodass andere Spieler das Wort nicht sehen
            try:
                secret_word_input = getpass("Das geheime Wort eingeben (Das kann keiner sehen :) ) (leer für zufällig / Q zum Schließen): ").strip()
            except (EOFError, KeyboardInterrupt):
                self.close()
                
            # Wenn die Eingabe leer gelassen wurde zufälliges Wort auswählen
            if secret_word_input == "":
                secret_word_input = random.choice(self.wordlist_content).strip()
                
            secret_word_input = self.convert_word_to_standard_characters(secret_word_input) # Sonderzeichen umwandeln
            secret_word_input_lower = secret_word_input.lower() # in Kleinbuchstaben umwandeln um es mit der Wortliste zu vergleichen
            
            # Programm beenden, wenn die Eingabe "q" war
            if secret_word_input_lower == "q":
                self.close()
            
            # Überprüft, ob das Wort ein valides deutsches Wort auf der Wortliste ist
            if not self.check_if_word_is_valid(secret_word_input_lower):
                print("Bitte gib ein gültiges deutsches Wort ein!")
            else:
                self.secret_word_lower = secret_word_input_lower
                self.secret_word_upper = secret_word_input_lower.upper()
    
    def get_user_input(self) -> str:
        """Fragt den Benutzer nach seinem nächsten Buchstaben oder Wort

        Returns:
            str: Benutzereingabe
        """
        
        user_input = ""
        while True:
            try:
                user_input = input("Gib deinen nächsten Buchstaben oder das Lösungswort ein: ").strip()
            except (EOFError, KeyboardInterrupt):
                self.close()
            if user_input != "":
                break
            else:
                self.print_gui()
            
        return user_input
        
    def check_if_word_is_valid(self, word: str):
        """Überprüft, ob das eingegebene Wort in der Wortliste enthalten ist

        Args:
            word (str): Wort, das überprüft werden soll

        Returns:
            bool: Ist das Wort in der Wortliste? 
        """
        
        if word in self.wordlist_content:
            return True
        else:
            return False
        
    def convert_word_to_standard_characters(self, word: str) -> str:
        """Erstetzt bestimmte Sonderzeichen mit ihren ASCII repräsentationen
        Args:
            word (str): Das Wort, in welchem die Sonderzeichen ersetzt werden sollen

        Returns:
            str: Das bearbeitete Wort
        """
        
        # Definiert die zu ersetzenden Buchstaben und mit was diese ersetzt werden sollen
        custom_mappings = {
            'ü': 'ue',
            'ö': 'oe',
            'ä': 'ae',
            'ß': 'ss'
        }
        
        # Sonderzeichen mit normalen Buchstaben ersetzen
        for char, replacement in custom_mappings.items():
            word = word.replace(char, replacement)
        
        return word
            
    def wait_for_keypress(self) -> None:
        """Wartet auf eine Benutzereingabe, bevor das Spiel fortgesetzt wird
        """
        try:
            user_input = input("Drücke Enter um Fortzufahren (Q zum Schließen) ")
            # Wenn der Benutzer "q" eingibt, wird das Programm geschlossen
            if user_input.lower() == "q":
                self.close()
                
        except (EOFError, KeyboardInterrupt):
            self.close()
        
    def game_finished(self, won: bool) -> None:
        """"Zeigt den Schluss-Bildschirm an

        Args:
            won (bool): Hat der Benutzer gewonnen?
        """
        
        self.print_gui()
        self.game_running = False
        
        # Ausgabe an den Benutzer, um ihn über das Spielende zu informieren
        if won:
            print("Du hast gewonnen! :) Gewonnen!!!") 
        else:
            print("Du hast verloren! :()")
        print(f"Das geheime Wort war ***{self.secret_word_lower.capitalize()}***")
        
        self.wait_for_keypress() # Warten, bis der Benutzer fortfahren möchte
        
    def close(self) -> None:
        """Schließt das Programm
        """
        
        sys.exit()
    
    
# Dieser Code soll nur ausgeführt werden, wenn das Programm direkt gestartet wird
if __name__ == "__main__":
    hangman_game = HangmanGame()
    hangman_game.start_game()