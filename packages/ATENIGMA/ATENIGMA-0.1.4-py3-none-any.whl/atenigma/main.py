import argparse
import os

from banner import show_banner
from decryption import decrypt
from encryption import encrypt


def encrypt_file(file_path: str, password: str, extension: str):
    with open(file_path, "r", encoding='utf-8') as k:
        message = k.read()
    encrypted, salt = encrypt(message, password)
    encrypted_file_path = os.path.splitext(file_path)[0] + extension
    with open(encrypted_file_path, 'wb', encoding='utf-8') as e:
        e.write(salt)
        e.write(encrypted)
    print(
        f'[*] File Encryption Completed\n[*] File name: {encrypted_file_path}')


def decrypt_file(file_path: str, password: str, extension: str):
    with open(file_path, 'rb', encoding='utf-8') as d:
        salt = d.read(16)
        encrypted_message = d.read()
    try:
        decrypted = decrypt(encrypted_message, password, salt)
        decrypted_file_path = file_path
        with open(decrypted_file_path+extension, 'w', encoding='utf-8') as t:
            t.write(decrypted)
        print(f'File decrypted and saved as {decrypted_file_path}')
    except:
        print("Invalid Password")


def main():
    parser = argparse.ArgumentParser(
        description="ATENIGMA Basic File encryption and decryption with password")
    parser.add_argument('--file',
                        help='Path to the file to be processed')
    parser.add_argument('--key', help='Give your password')
    parser.add_argument('--encrypt', action='store_true',
                        help='Encrypt the file or data')
    parser.add_argument('--decrypt', action='store_true',
                        help='Decrypt the file or data')
    parser.add_argument('--showbanner', action='store_true',
                        help='Show the banner of the tool')
    parser.add_argument('--exten', default='.enc',
                        help='File extension for encrypted/decrypted files')

    args = parser.parse_args()
    file_path = args.file
    password = args.key

    if args.encrypt:
        encrypt_file(file_path, password, args.exten)
    elif args.decrypt:
        decrypt_file(file_path, password, args.exten)
    elif args.showbanner:
        show_banner()
    else:
        print("[!] No action selected (encrypt or decrypt)")


if __name__ == '__main__':
    main()
