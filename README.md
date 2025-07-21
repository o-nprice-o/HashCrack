# HashCrack.py

HashCrack.py is a versatile Python tool for cracking hashed passwords. It supports MD5, SHA1, and SHA256 hashes and offers multiple cracking methods including wordlist attacks, CPU multiprocessing brute force, and GPU-accelerated brute force via Hashcat.

---

## Features

- Automatically detects hash type (MD5, SHA1, SHA256) based on hash length
- Auto-detects available wordlists in the `wordlists/` directory
- Lets users select wordlists or choose brute force cracking
- CPU-based multiprocessing brute force to speed up cracking
- GPU-based brute force support via Hashcat for fast cracking on compatible hardware
- Gracefully handles input errors and allows retrying without restarting
- Supports UTF-8 encoded wordlists and ignores file errors

---

## Getting Started

### Prerequisites

- Python 3.x installed
- [Hashcat](https://hashcat.net/hashcat/) installed and available in system PATH (for GPU brute force)
- Basic command line knowledge

### Installation
Clone the repository:

```
   git clone https://github.com/o-nprice-o/HashCrack.git
```
Navigate into the project folder:

    cd HashCrack

Place your .txt wordlists inside the wordlists/ folder or use the included sample lists.


## Usage

Run the script:

python HashCrack.py

You will be prompted to:

- Enter the hash to crack (or type exit to quit)

- Choose a cracking method:
    - Wordlist attack
    - CPU multiprocessing brute force (specify max password length)
    - GPU brute force using Hashcat (requires Hashcat installed)

- If applicable, select a wordlist from available options

If the hash is cracked, the plaintext password will be displayed.

## Wordlists

The wordlists/ folder contains themed wordlists such as:

- CommonPasswords.txt — frequently used passwords

- WVUWordlist.txt — West Virginia University themed words

- CarThemedWordlist.txt — car-related words

- TechTerms.txt — common technology terms

Add your own .txt wordlists to the folder; the program auto-detects them.
Contributing

Feel free to open issues or submit pull requests for improvements!

## License

This project is released under the MIT License.

## Contact
Created by Nicholas Price
