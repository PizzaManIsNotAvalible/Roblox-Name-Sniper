import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import sleep
from colorama import Fore, Style, init

init()

def check_username(username):
    url = f"https://auth.roblox.com/v1/usernames/validate?Username={username}&Birthday=2000-01-01"
    retries = 3  # Retry up to 3 times
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=5)  # Add timeout to prevent hanging
            response.raise_for_status()  # Raise HTTP errors if any
            response_data = response.json()

            code = response_data.get("code")
            if code == 0:
                print(Fore.GREEN + f"VALID: {username}" + Style.RESET_ALL)
            elif code == 1:
                print(Fore.LIGHTBLACK_EX + f"TAKEN: {username}" + Style.RESET_ALL)
            elif code == 2:
                print(Fore.RED + f"CENSORED: {username}" + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + f"Unknown code ({code}): {username}" + Style.RESET_ALL)
            return  # Exit the loop if successful

        except requests.exceptions.RequestException as e:
            print(Fore.YELLOW + f"Error with {username} (attempt {attempt + 1}): {e}" + Style.RESET_ALL)
            sleep(1)  # Wait 1 second before retrying

    print(Fore.RED + f"Failed to process {username} after {retries} attempts." + Style.RESET_ALL)

def main():
    with open("usernames.txt", "r") as file:
        usernames = file.read().splitlines()

    # Use ThreadPoolExecutor with reduced workers
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Use as_completed to handle errors and progress tracking
        futures = {executor.submit(check_username, username): username for username in usernames}
        for future in as_completed(futures):
            username = futures[future]
            try:
                future.result()  # Trigger execution and catch any exceptions
            except Exception as e:
                print(Fore.RED + f"Unhandled exception for {username}: {e}" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
