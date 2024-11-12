from ascii_art import get_hangmans
import urllib.request
import os
import json

class HangmanGame:
    def __init__(self) -> None:
        # Variablen auf Standartwert initialisieren
        self.easy_mode = None
        
        self.secret_word = None
        self.guessed_letters = []
        self.right_letters = []
        self.num_wrong_words = 0
        
        self.hangmans = get_hangmans()
        
        self.wordlist_link = "https://raw.githubusercontent.com/Jonny-exe/German-Words-Library/refs/heads/master/German-words-1600000-words-multilines.json"
        self.wordlist_path = "german_words.json"
        
        self.download_wordlist()
        self.prepare_wordlist()
        
    def start_game(self) -> None:
        while True:
            self.get_game_settings()
        
    ################ WIP ##################
    def check_if_word_is_valid(self, word: str):
        print(self.wordlist_content)
        if word in self.wordlist_content:
            return True
        else:
            return False
        
    def get_game_settings(self) -> None:
        """Geheimes Wort und den "Spielmodus" vom Benutzer bekommen
        """
        
        # Variablen zurücksetzen, falls sie bereits beschrieben wurden
        self.secret_word = None
        self.easy_mode = None
        
        # Usereingabe für das geheime Wort bekommen und überprüfen, ob es ein valides deutsches Wort ist
        self.get_secret_word()
        
        self.ask_game_mode()
        
    def print_gui(self) -> None:
        number_wrong_words = len(self.guessed_letters)
        print(self.hangmans[number_wrong_words])
        pass
    
    def generate_word_output(self) -> list:
        word_output = ["_"]*len(self.secret_word)
        for char in self.right_letters:
            for i, letter in enumerate(self.secret_word):
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
            common_words = set(word.lower() for word in json.load(f))
            
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
        while self.secret_word == None:
            secret_word_input = input("Bitte gib das geheime Wort ein (ohne, dass die anderen Mitspieler zuschauen!): ")
            err = self.check_if_word_is_valid(secret_word_input)
            if not err:
                print("Bitte gib ein gültiges deutsches Wort ein!")
            else:
                self.secret_word = secret_word_input
            
if __name__ == "__main__":
    hangman_game = HangmanGame()
    hangman_game.start_game()