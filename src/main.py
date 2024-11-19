print("Importing...")
from ascii_art import get_hangmans
import urllib.request
import os
import json
import random
import string
import time
import sys
from getpass import getpass

# Used to convert non-ASCII characters into the best ASCII representation
try:
    from unidecode import unidecode
except ModuleNotFoundError:
    os.system('pip install unidecode')
    from unidecode import unidecode

print("Imported!")

class HangmanGame:
    def __init__(self) -> None:
        # Variablen auf Standardwert initialisieren
        self.set_variables()
        self.clear_console()
        
        self.hangmans = get_hangmans()
        
        self.wordlist_link = "https://raw.githubusercontent.com/Jonny-exe/German-Words-Library/refs/heads/master/German-words-1600000-words-multilines.json"
        self.wordlist_path = "german_words.json"
        
        # Wortliste vorpereiten
        self.download_wordlist()
        self.prepare_wordlist()
        
    def set_variables(self) -> None:
        """Variablen auf ihren Standardwert setzten
        """
        self.easy_mode = None
        self.game_running = None
        
        self.secret_word_upper = None
        self.secret_word_lower = None
        self.guessed_letters = []
        self.wrong_letters = []
        self.right_letters = []
        self.lives_remaining_default = 6
        self.lives_remaining = self.lives_remaining_default
        self.num_wrong_words = 0
        self.revealed_word = None
        
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
                
                ###################### WIP #######################
                if not right_input:
                    self.lives_remaining -= 1
                
                if self.lives_remaining == 0:
                    self.game_finished(won=False)
                
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
                self.game_finished(won=True)
                return True
            else:
                return False
            
        else:
            self.guessed_letters.append(user_input_upper)
            
            # Wenn der einfache Modus aktiviert ist und der Spieler einen Buchstaben versucht, der bereits versucht wurde, verliert er kein Leben
            if (user_input_upper in self.right_letters or user_input_upper in self.wrong_letters) and self.easy_mode:
                return True
            # Sonst Unterscheidung, ob der Buchstabe richtig war und Anhängen an das zugehörige Array
            elif user_input_upper in self.secret_word_upper:
                self.right_letters.append(user_input_upper)
                return True
            else:
                self.wrong_letters.append(user_input_upper)
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
        self.revealed_word = ""
        
        word_output = ["_"] * len(self.secret_word_upper)
        
        right_letters_set = set(self.right_letters)
        
        for i, letter in enumerate(self.secret_word_upper):
            if letter in right_letters_set:
                word_output[i] = letter
                self.revealed_word += letter
                
        self.revealed_word = self.revealed_word.lower()
                    
        return word_output
    
    ########################################################################################
    
    def download_wordlist(self):
        print("Wortliste überprüfen")
        if not os.path.exists(self.wordlist_path):
            print("Wortliste wird heruntergeladen...")
            urllib.request.urlretrieve(self.wordlist_link, self.wordlist_path)
            print("Wortliste erfolgreich heruntergeladen.")
        else:
            print("Wortliste bereits vorhanden.")
            
    def prepare_wordlist(self):
        print("Loading Wordlist...")
        with open(self.wordlist_path, "r", encoding="utf-8") as f:
            common_words = list(self.convert_word_to_standard_characters(word.lower()) for word in json.load(f))
        print("Wordlist loaded")
            
        self.wordlist_content = common_words
            
    def ask_game_mode(self):
    # Usereingabe für die Einstellung des Easy-Modes und überprüfen, ob die Eingabe valide ist
        while self.easy_mode == None:
            # easy_mode_input = input("Möchtest du den einfachen Modus aktivieren? (Y/N): ")
            try:
                easy_mode_input = input("Möchtest du den einfachen Modus aktivieren? (Y / N, Enter / Q zum Schließen): ").lower()
            except (EOFError, KeyboardInterrupt):
                self.close()
            
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
        while self.secret_word_upper == None:
            try:
                secret_word_input = getpass("Das geheime Wort eingeben (Das kann keiner sehen :) ) (leer für zufällig / Q zum Schließen): ").strip()
            except (EOFError, KeyboardInterrupt):
                self.close()
                
            if secret_word_input == "":
                secret_word_input = random.choice(self.wordlist_content).strip()
                
            secret_word_input = self.convert_word_to_standard_characters(secret_word_input)
                
            secret_word_input_lower = secret_word_input.lower()
            
            if secret_word_input_lower == "q":
                self.close()
                
            
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
        """ Überprüft, ob das eingegebene Wort in der Wortliste enthalten ist
        """
        if word in self.wordlist_content:
            return True
        else:
            return False
        
    def convert_word_to_standard_characters(self, word: str) -> str:
        custom_mappings = {
            'ü': 'ue',
            'ö': 'oe',
            'ä': 'ae',
            'ß': 'ss'
        }
        
        for char, replacement in custom_mappings.items():
            word = word.replace(char, replacement)
        
        return unidecode(word)
            
    def wait_for_keypress(self) -> None:
        """Wartet auf eine Benutzereingabe, bevor das Spiel fortgesetzt wird
        """
        input("Drücke Enter um Fortzufahren ")
        
    def game_finished(self, won: bool) -> None:
        self.print_gui()
        
        self.game_running = False
        
        if won:
            print("Du hast gewonnen! :) Gewonnen! (Hallo mein Lieber, Hast du ein Wort? KRATER!!)")
        else:
            print("Du hast verloren! :()")
        
        print(f"Das geheime Wort war ***{self.secret_word_lower.capitalize()}***")
        self.wait_for_keypress()
        
    def close(self) -> None:
        sys.exit()
            
if __name__ == "__main__":
    hangman_game = HangmanGame()
    hangman_game.start_game()