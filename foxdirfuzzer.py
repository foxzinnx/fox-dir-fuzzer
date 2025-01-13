import requests
from colorama import Fore, Style, init
import argparse

init(autoreset=True)

def main_menu():
    banner = f"""{Fore.RED}
  █████▒▒█████  ▒██   ██▒   ▓█████▄  ██▓ ██▀███       █████▒█    ██ ▒███████▒▒███████▒▓█████  ██▀███  
▓██   ▒▒██▒  ██▒▒▒ █ █ ▒░   ▒██▀ ██▌▓██▒▓██ ▒ ██▒   ▓██   ▒ ██  ▓██▒▒ ▒ ▒ ▄▀░▒ ▒ ▒ ▄▀░▓█   ▀ ▓██ ▒ ██▒
▒████ ░▒██░  ██▒░░  █   ░   ░██   █▌▒██▒▓██ ░▄█ ▒   ▒████ ░▓██  ▒██░░ ▒ ▄▀▒░ ░ ▒ ▄▀▒░ ▒███   ▓██ ░▄█ ▒
░▓█▒  ░▒██   ██░ ░ █ █ ▒    ░▓█▄   ▌░██░▒██▀▀█▄     ░▓█▒  ░▓▓█  ░██░  ▄▀▒   ░  ▄▀▒   ░▒▓█  ▄ ▒██▀▀█▄  
░▒█░   ░ ████▓▒░▒██▒ ▒██▒   ░▒████▓ ░██░░██▓ ▒██▒   ░▒█░   ▒▒█████▓ ▒███████▒▒███████▒░▒████▒░██▓ ▒██▒
 ▒ ░   ░ ▒░▒░▒░ ▒▒ ░ ░▓ ░    ▒▒▓  ▒ ░▓  ░ ▒▓ ░▒▓░    ▒ ░   ░▒▓▒ ▒ ▒ ░▒▒ ▓░▒░▒░▒▒ ▓░▒░▒░░ ▒░ ░░ ▒▓ ░▒▓░
 ░       ░ ▒ ▒░ ░░   ░▒ ░    ░ ▒  ▒  ▒ ░  ░▒ ░ ▒░    ░     ░░▒░ ░ ░ ░░▒ ▒ ░ ▒░░▒ ▒ ░ ▒ ░ ░  ░  ░▒ ░ ▒░
 ░ ░   ░ ░ ░ ▒   ░    ░      ░ ░  ░  ▒ ░  ░░   ░     ░ ░    ░░░ ░ ░ ░ ░ ░ ░ ░░ ░ ░ ░ ░   ░     ░░   ░ 
           ░ ░   ░    ░        ░     ░     ░                  ░       ░ ░      ░ ░       ░  ░   ░     
                             ░                                      ░        ░                       
                                    {Fore.CYAN}github.com/foxzinnx                                
                                                                                                        """

    print(banner)

def server_version(target):
    try:
        response = requests.head(target)
        server = response.headers.get('Server')
        if server:
            print(f"{Fore.YELLOW}Server: {Fore.CYAN}{server}")
        else:
            print(f"{Fore.RED}Could not retrieve the server version.")
    except requests.RequestException as e:
        print(f"{Fore.RED}[!] Error accessing {target} {e}")


def brute_force(target, wordlist):
    try:
        with open(wordlist, "r") as archive:
            directory = archive.readlines()

            print(f"{Fore.YELLOW}Starting brute force on target: {Fore.CYAN}{target}")

            for directories in directory:
                directories = directories.strip()
                url = f"{target}/{directories}"

                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        print(f"{Fore.GREEN}[+] Directory found: {Fore.LIGHTCYAN_EX}{url} ({Fore.YELLOW}Status code: {Fore.GREEN}{response.status_code})")
                    elif 300 <= response.status_code < 400:
                        print(f"{Fore.YELLOW}[~] Redirection detected: {Fore.CYAN}{url} ({Fore.YELLOW}Status Code: {response.status_code})")
                    elif response.status_code == 403:
                        print(f"{Fore.RED}Access forbidden! ({Fore.YELLOW}Status code: {Fore.RED}{response.status_code})")
                
                except requests.RequestException as e:
                    print(f"[!] Error accessing {url}: {e}")

    except FileNotFoundError:
        print(f"{Fore.RED}Wordlist not found")

    except Exception as e:
        print(f"{Fore.RED}An error occurred {url}: {e}")

def main():
    main_menu()

    parser = argparse.ArgumentParser(description=f"{Fore.RED}FOX - {Fore.YELLOW}DIR FUZZER")
    parser.add_argument("-t", "--target", required=True, help="Target URL (e.g., http://example.com)")
    parser.add_argument("-w", "--wordlist", required=True, help="Wordlist path")

    args = parser.parse_args()
    target = args.target
    wordlist = args.wordlist

    if not target.startswith(("http://", "https://")):
        print(f"{Fore.RED}[!] Invalid URL. Make sure it starts with 'http://' or 'https://'.")
        exit()

    server_version(target)
    brute_force(target, wordlist)

if __name__ == "__main__":
    main()