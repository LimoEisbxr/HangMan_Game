def get_hangmans():
	"""Lädt die ASCII HangMans

	Returns:
		list: Liste mit den ASCII HangMans
	"""

	hangmans = [r'''
    +---+
    |   |
        |
        |
        |
        |
  =========''', r'''
    +---+
    |   |
    O   |
        |
        |
        |
  =========''', r'''
    +---+
    |   |
    O   |
    |   |
        |
        |
  =========''', r'''
    +---+
    |   |
    O   |
   /|   |
        |
        |
  =========''', r'''
    +---+
    |   |
    O   |
   /|\  |
        |
        |
  =========''', r'''
    +---+
    |   |
    O   |
   /|\  |
   /    |
        |
  =========''', r'''
    +---+
    |   |
    O   |
   /|\  |       
   / \  |
        |
  =========''']
    
	return hangmans

# Wenn die Datei direkt ausgeführt wird, werden die HangMans ausgegeben
if __name__ == "__main__":
    print(get_hangmans())