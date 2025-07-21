import hashlib
import os
import sys

def choose_wordlist():
    wordlists_dir = 'wordlists'
    wordlists = [f for f in os.listdir(wordlists_dir) if f.endswith('.txt')]

    if not wordlists:
        print("No wordlists found in the 'wordlists' directory.")
        sys.exit(1)

    print("\nHere are the available wordlists:")
    for idx, wordlist in enumerate(wordlists, 1):
        print(f"{idx}. {wordlist}")

    while True:
        try:
            choice = int(input("Which wordlist would you like to use? (Enter a number): "))
            if 1 <= choice <= len(wordlists):
                selected = os.path.join(wordlists_dir, wordlists[choice - 1])
                print(f"\n Selected: {wordlists[choice - 1]}")
                return selected
            else:
                print("Please enter a valid number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def detect_hash_type(hash_str):
    length = len(hash_str)
    if length == 32:
        return 'md5'
    elif length == 40:
        return 'sha1'
    elif length == 64:
        return 'sha256'
    else:
        return None

def crack_hash(hash_to_crack, wordlist_path, hash_type):
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            for word in f:
                word = word.strip()
                hashed_word = hashlib.new(hash_type, word.encode()).hexdigest()
                if hashed_word == hash_to_crack:
                    print(f"\nSuccess! Hash cracked: {word}")
                    return word
    except FileNotFoundError:
        print(f"Wordlist file not found: {wordlist_path}")
        sys.exit(1)

    print("\nNo match found in the selected wordlist.")
    return None

def main():
    print("\n=== HashCrack.py ===")
    while True:
        try:
            hash_input = input("\nEnter the hash to crack (or type 'exit' to quit): ").strip().lower()
            if hash_input == 'exit':
                print("Exiting HashCrack.py. Goodbye!")
                break

            hash_type = detect_hash_type(hash_input)
            if not hash_type:
                print("\nUnsupported or unknown hash type. Only MD5, SHA1, and SHA256 are supported.")
                continue  # retry

            print(f"\n🔍 Detected hash type: {hash_type.upper()}")

            wordlist_path = choose_wordlist()
            if not wordlist_path:
                print("No wordlist selected. Please try again.")
                continue

            crack_hash(hash_input, wordlist_path, hash_type)

            # After cracking attempt, ask if they want to try another
            again = input("\nDo you want to try another hash? (y/n): ").strip().lower()
            if again != 'y':
                print("Thanks for using HashCrack.py!")
                break

        except KeyboardInterrupt:
            print("\nInterrupted by user. Exiting.")
            break

        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            print("Please try again.")

if __name__ == "__main__":
    main()

