import requests
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from colorama import Fore, Style, init

init()

def check_username(username):
    url = f"https://auth.roblox.com/v1/usernames/validate?Username={username}&Birthday=2000-01-01"
    try:
        response = requests.get(url)
        response_data = response.json()

        code = response_data.get("code")
        if code == 0:
            print(Fore.GREEN + f"VALID: {username}" + Style.RESET_ALL)
        elif code == 1:
            print(Fore.LIGHTBLACK_EX + f"TAKEN: {username}" + Style.RESET_ALL)
        elif code == 2:
            print(Fore.RED + f"CENSORED: {username}" + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + f"bruh ({code}): {username}" + Style.RESET_ALL)

    except requests.exceptions.RequestException as e:
        print(Fore.YELLOW + f"glitch {username}: {e}" + Style.RESET_ALL)
    
    # Add a small delay to respect the server
    sleep(0.5)

def main():
    with open("usernames.txt", "r") as file:
        usernames = file.read().splitlines()

    # Use ThreadPoolExecutor with reduced workers
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(check_username, usernames)

if __name__ == "__main__":
    main()
