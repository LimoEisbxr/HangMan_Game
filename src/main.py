from ascii_art import get_hangmans
import urllib.request
import os
import json
import random

class HangmanGame:
    def __init__(self) -> None:
        # Variablen auf Standartwert initialisieren
        self.easy_mode = None
        self.game_running = None
        
        self.secret_word_upper = None
        self.secret_word_lower = None
        self.wrong_letters = []
        self.right_letters = []
        self.num_wrong_words = 0
        self.lives_remaining = 6
        
        self.hangmans = get_hangmans()
        
        self.wordlist_link = "https://raw.githubusercontent.com/Jonny-exe/German-Words-Library/refs/heads/master/German-words-1600000-words-multilines.json"
        self.wordlist_path = "german_words.json"
        
        # Wortliste vorpereiten
        self.download_wordlist()
        self.prepare_wordlist()
        
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
                right_input, game_won = self.process_user_input(user_input)
                
                ###################### WIP #######################
                if not right_input:
                    self.lives_remaining -= 1
                    
                if self.lives_remaining == 0:
                    self.game_running = False
                    # printe was zum Tod hier
                    
                if game_won:
                    self.game_running = False
                    # printe was schönes hier zum feierlichen Sieg
                    print(f"Das geheime Wort war {self.secret_word_lower.capitalize()}")
    
    def get_game_settings(self) -> None:
        """Geheimes Wort und den "Spielmodus" vom Benutzer bekommen
        """
        
        # Variablen zurücksetzen, falls sie bereits beschrieben wurden
        self.secret_word_upper = None
        self.secret_word_lower = None
        self.easy_mode = None
        self.right_letters = []
        self.wrong_letters = []
        self.lives_remaining = 6
        
        # Usereingabe für das geheime Wort bekommen und überprüfen, ob es ein valides deutsches Wort ist
        self.clear_console()
        self.get_secret_word()
        self.clear_console()
        
        # Usereingabe für den "Spielmodus" bekommen
        self.ask_game_mode()
        
    def get_user_input(self) -> str:
        """Fragt den Benutzer nach seinem nächsten Buchstaben oder Wort

        Returns:
            str: Benutzereingabe
        """
        user_input = ""
        while user_input == "":
            user_input = input("Gib deinen nächsten Buchstaben oder das Lösungswort ein: ")
            
        return user_input
    
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
                return True, True
            else:
                return False, False
            
        else:
            # Wenn der einfache Modus aktiviert ist und der Spieler einen Buchstaben versucht, der bereits versucht wurde, verliert er kein Leben
            if (user_input_upper in self.right_letters or user_input_upper in self.wrong_letters) and self.easy_mode:
                return True, False
                
            # Sonst Unterscheidung, ob der Buchstabe richtig war und Anhängen an das zugehörige Array
            elif user_input_upper in self.secret_word_upper:
                self.right_letters.append(user_input_upper)
                return True, False
            else:
                self.wrong_letters.append(user_input_upper)
                return False, False
        
    def print_gui(self) -> None:
        """"Benutzeroberfläche" ausgeben
        """
        
        self.clear_console()
        
        # Hangman ausgeben, der zu den aktuellen Leben passt
        number_wrong_words = len(self.wrong_letters)
        print(self.hangmans[number_wrong_words])
        
        # Wort ausgeben, das Unterstriche als Lücken für noch nicht erratene Buchstaben hat
        word_output = self.generate_word_output()
        print(" ".join(word_output))
    
    def clear_console(self) -> None:
        """Konsole leeren
        """
        
        os.system("cls" if os.name == "nt" else "clear")
    
    def generate_word_output(self) -> list:
        word_output = ["_"]*len(self.secret_word_upper)
        for char in self.right_letters:
            for i, letter in enumerate(self.secret_word_upper):
                if letter == char:
                    word_output[i] = char
                    
        return word_output
    
    ########################################################################################
    
    def download_wordlist(self):
        if not os.path.exists(self.wordlist_path):
            print("Wortliste wird heruntergeladen...")
            urllib.request.urlretrieve(self.wordlist_link, self.wordlist_path)
            print("Wortliste erfolgreich heruntergeladen.")
        else:
            print("Wortliste bereits vorhanden.")
            
    def prepare_wordlist(self):
        with open(self.wordlist_path, "r", encoding="utf-8") as f:
            common_words = list(word.lower() for word in json.load(f))
            
        self.wordlist_content = common_words
            
    def ask_game_mode(self):
    # Usereingabe für die Einstellung des Easy-Modes und überprüfen, ob die Eingabe valide ist
        while self.easy_mode == None:
            easy_mode_input = input("Möchtest du den einfachen Modus aktivieren? (Y/N): ")
            if easy_mode_input == "Y":
                self.easy_mode = True
            elif easy_mode_input == "N":
                self.easy_mode = False
            else:
                print("Ungültige Eingabe! - mögliche Eingaben: Y - N")
                
    def get_secret_word(self):
        while self.secret_word_upper == None:
            secret_word_input = input("Bitte gib das geheime Wort ein (ohne, dass die anderen Mitspieler zuschauen! / für ein zufälliges Wort leer lassen): ").strip()
            if secret_word_input == "":
                # secret_word_num = random.randint(0, len(self.wordlist_content) - 1)
                # secret_word_input = self.wordlist_content[secret_word_num]
                secret_word_input = random.choice(self.wordlist_content).strip()
                
            secret_word_input_lower = secret_word_input.lower()
            err = self.check_if_word_is_valid(secret_word_input_lower)
            if not err:
                print("Bitte gib ein gültiges deutsches Wort ein!")
            else:
                self.secret_word_upper = secret_word_input.upper()
                self.secret_word_lower = secret_word_input_lower
                
    def check_if_word_is_valid(self, word: str):
        # print(self.wordlist_content)
        if word in self.wordlist_content:
            return True
        else:
            return False
            
if __name__ == "__main__":
    hangman_game = HangmanGame()
    hangman_game.start_game()