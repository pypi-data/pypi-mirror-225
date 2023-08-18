#! /usr/bin/python
from colored import Back, Fore, Style


def show_banner():
    txt = """
 █████╗ ████████╗███████╗███╗   ██╗██╗ ██████╗ ███╗   ███╗ █████╗ 
██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██║██╔════╝ ████╗ ████║██╔══██╗
███████║   ██║   █████╗  ██╔██╗ ██║██║██║  ███╗██╔████╔██║███████║
██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██║██║   ██║██║╚██╔╝██║██╔══██║
██║  ██║   ██║   ███████╗██║ ╚████║██║╚██████╔╝██║ ╚═╝ ██║██║  ██║
╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝
"""
    print(f'{Fore.GREEN}{txt}{Style.reset}')
    print(f"{Fore.GREEN}[*] Version 1.0.0{Style.reset}")
    print(f"{Fore.YELLOW}[*] Secure your files with ATENIGMA{Style.reset}")
    print(
        f"{Fore.YELLOW}[*] Encrypted files are safe and sound{Style.reset}")
    print(f"{Fore.YELLOW}[*] Author: Prasaanth{Style.reset}")
    print(
        f"{Fore.BLUE}[*] GitHub: https://github.com/yourusername/atenigma{Style.reset}")
