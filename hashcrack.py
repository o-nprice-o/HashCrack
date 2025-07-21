import hashlib
import os
import sys
import string
import itertools
import subprocess
from multiprocessing import Pool, Manager, cpu_count

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

def hashcat_mode(hash_type):
    return {
        'md5': '0',
        'sha1': '100',
        'sha256': '1400'
    }.get(hash_type, None)

def crack_hash(hash_to_crack, wordlist_path, hash_type):
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            for count, word in enumerate(f, 1):
                word = word.strip()
                hashed_word = hashlib.new(hash_type, word.encode()).hexdigest()
                if hashed_word == hash_to_crack:
                    print(f"\nSuccess! Hash cracked: {word} (attempt #{count})")
                    return word
    except FileNotFoundError:
        print(f"Wordlist file not found: {wordlist_path}")
        sys.exit(1)

    print("\nNo match found in the selected wordlist.")
    return None

def hash_matches(args):
    prefix, hash_to_crack, hash_type, max_length, chars, found_flag = args
    if found_flag.is_set():
        return None
    for length in range(len(prefix), max_length + 1):
        for suffix in itertools.product(chars, repeat=length - len(prefix)):
            if found_flag.is_set():
                return None
            attempt = prefix + ''.join(suffix)
            hashed_attempt = hashlib.new(hash_type, attempt.encode()).hexdigest()
            if hashed_attempt == hash_to_crack:
                found_flag.set()
                return attempt
    return None

def multiprocessing_brute_force(hash_to_crack, hash_type, max_length=4):
    chars = string.ascii_lowercase
    found_flag = Manager().Event()
    pool = Pool(cpu_count())

    prefixes = chars  # split search by first char
    args = [(prefix, hash_to_crack, hash_type, max_length, chars, found_flag) for prefix in prefixes]

    print(f"\nStarting multiprocessing brute force using {cpu_count()} CPU cores...")
    results = pool.map(hash_matches, args)
    pool.close()
    pool.join()

    for result in results:
        if result:
            print(f"\nSuccess! Hash cracked: {result}")
            return result

    print("\nNo match found with multiprocessing brute force.")
    return None

def gpu_brute_force_hashcat(hash_to_crack, hash_type):
    hashcat_path = 'hashcat'  # assumes in PATH
    mode = hashcat_mode(hash_type)
    if not mode:
        print("Unsupported hash type for GPU cracking.")
        return

    hash_file = 'hash_input.txt'
    with open(hash_file, 'w') as f:
        f.write(hash_to_crack)

    print(f"\nLaunching Hashcat (mode {mode}) for GPU brute force...")
    command = [
        hashcat_path,
        '-a', '3',               # brute force mode
        '-m', mode,              # hash type
        hash_file,
        '?l?l?l?l',              # example pattern: 4 lowercase letters
        '--force',
        '--quiet'
    ]

    try:
        subprocess.run(command, check=True)
        subprocess.run([hashcat_path, '-m', mode, hash_file, '--show'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\nHashcat failed: {e}")
    finally:
        os.remove(hash_file)

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
                continue

            print(f"\n🔍 Detected hash type: {hash_type.upper()}")
            print("\nChoose cracking method:")
            print("1. Wordlist")
            print("2. Brute Force (multiprocessing, CPU)")
            print("3. Brute Force Fast Cracking (dGPU via Hashcat)")
            method = input("Enter 1, 2, or 3: ").strip()

            if method == '1':
                wordlist_path = choose_wordlist()
                crack_hash(hash_input, wordlist_path, hash_type)

            elif method == '2':
                while True:
                    try:
                        max_len = int(input("Enter max password length for brute force (e.g., 4): "))
                        if max_len > 0:
                            break
                        else:
                            print("Please enter a positive integer.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                multiprocessing_brute_force(hash_input, hash_type, max_len)

            elif method == '3':
                gpu_brute_force_hashcat(hash_input, hash_type)

            else:
                print("Invalid option. Please enter 1, 2, or 3.")
                continue

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
