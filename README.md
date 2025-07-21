# HashCrack.py

HashCrack.py is a simple Python tool for cracking hashed passwords using wordlists. It supports MD5, SHA1, and SHA256 hashes and allows you to select from multiple themed wordlists to try cracking the hash.

---

## Features

- Detects hash type automatically (MD5, SHA1, SHA256) based on hash length
- Auto-detects available wordlists in the `wordlists/` directory
- Lets the user choose which wordlist to use for cracking
- Gracefully handles input errors and allows retrying without restarting
- Supports wordlists with UTF-8 encoding and ignores errors in files

---

## Getting Started

### Prerequisites

- Python 3.x installed
- Basic command line knowledge

### Installation

1. Clone the repository:

```
git clone https://github.com/o-nprice-o/HashCrack.git
```

Navigate into the project folder:

```
cd HashCrack
```

Place your wordlists in the wordlists/ folder or use the included sample lists.

## Usage

Run the script:

```
python HashCrack.py
```

You will be prompted to:

- Enter the hash to crack (or type exit to quit)

- Select a wordlist from the displayed options

If a match is found, the plaintext password will be displayed.

## Wordlists

The wordlists/ folder contains themed wordlists, such as:

    CommonPasswords.txt — frequently used passwords

    WVUWordlist.txt — West Virginia University themed words

    CarThemedWordlist.txt — car-related words

    TechTerms.txt — common technology terms

You can add your own .txt wordlists to the folder; the program will detect them automatically.

## Contributing

Feel free to open issues or submit pull requests for improvements!

## License

This project is released under the MIT License.

## Contact

Created by Nicholas Price
