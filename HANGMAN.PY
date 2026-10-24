import random

# Configuration Constants
MAX_MISTAKES = 6
WORDS_FILE = "words.txt"

# ASCII Art stages for 0 to 6 incorrect guesses
HANGMAN_STAGES = [
    """
       ------
       |    |
            |
            |
            |
            |
    ---------
    """,
    """
       ------
       |    |
       O    |
            |
            |
            |
    ---------
    """,
    """
       ------
       |    |
       O    |
       |    |
            |
            |
    ---------
    """,
    """
       ------
       |    |
       O    |
      /|    |
            |
            |
    ---------
    """,
    """
       ------
       |    |
       O    |
      /|\\   |
            |
            |
    ---------
    """,
    """
       ------
       |    |
       O    |
      /|\\   |
      /     |
            |
    ---------
    """,
    """
       ------
       |    |
       O    |
      /|\\   |
      / \\   |
            |
    ---------
    """
]


def load_word_pool(filename):
    """Loads and sanitizes words from the external text file with a fallback."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            words = [line.strip().upper() for line in f if line.strip()]
            if not words:
                raise ValueError("Word file is empty.")
            return words
    except (FileNotFoundError, ValueError) as e:
        print(f"[!] Notice: {e} Using default word list.")
        return ["PYTHON", "DEVELOPER", "TERMINAL", "HANGMAN", "PROGRAMMING"]


def get_masked_word(secret_word, guessed_letters):
    """Generates the masked string representation of the secret word (e.g., _ A _ H E O N)."""
    return " ".join([char if char in guessed_letters else "_" for char in secret_word])


def play_round(word_pool):
    """Executes a single round of the Hangman game."""
    secret_word = random.choice(word_pool)
    guessed_letters = set()
    incorrect_guesses = 0

    print("\n" + "=" * 32)
    print("      TERMINAL HANGMAN")
    print("=" * 32)

    while incorrect_guesses < MAX_MISTAKES:
        print(HANGMAN_STAGES[incorrect_guesses])
        print(f"Word:   {get_masked_word(secret_word, guessed_letters)}")
        
        used_display = ", ".join(sorted(guessed_letters)) if guessed_letters else "None"
        print(f"Guessed: {used_display}")
        print(f"Lives:   {MAX_MISTAKES - incorrect_guesses}\n")

        guess = input("Guess a letter: ").strip().upper()

        # Input validation
        if not guess.isalpha() or len(guess) != 1:
            print("[!] Invalid input. Please enter a single alphabetical letter.\n")
            continue

        # Prevent duplicate penalty deduction
        if guess in guessed_letters:
            print(f"[!] You already tried '{guess}'. No penalty.\n")
            continue

        guessed_letters.add(guess)

        # Check guess against the secret word
        if guess in secret_word:
            print(f"[+] Correct! '{guess}' is in the word.\n")
            
            # Check victory condition
            if set(secret_word).issubset(guessed_letters):
                print(f"Victory! You successfully guessed the word: {secret_word}\n")
                return
        else:
            incorrect_guesses += 1
            print(f"[-] Incorrect. '{guess}' is not in the word.\n")

    # Defeat condition
    print(HANGMAN_STAGES[MAX_MISTAKES])
    print("GAME OVER! You ran out of attempts.")
    print(f"The secret word was: {secret_word}\n")


def main():
    word_pool = load_word_pool(WORDS_FILE)
    
    while True:
        play_round(word_pool)
        replay = input("Play again? (y/n): ").strip().lower()
        if replay != 'y':
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()