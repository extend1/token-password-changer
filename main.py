import requests, os, hashlib, time, json, string, random
from threading import RLock, Thread
from colorama import init, Fore, Style, Back
from colorama import init as colorama_init
from pystyle import Add, Center, Anime, Colors, Colorate, Write, System 
import secrets


config = json.load(open('./data/config.json', 'r'))

class SynchronizedEcho(object):
    print_lock = RLock()

    def __init__(self, global_lock=True):
        if not global_lock:
            self.print_lock = RLock()

    def __call__(self, msg):
        with self.print_lock:
            print(msg)

def randomPassword(length):
    all = string.ascii_lowercase + string.ascii_uppercase +  string.digits
    passw = "".join(random.sample(all, length))
    return passw

def getheaders(Token):
    header = {
        'Authorization': Token,
		'accept': '*/*',
		'accept-language': 'en-US',
		'connection': 'keep-alive',
		'cookie': f'__cfduid = {secrets.token_hex(43)}; __dcfduid={secrets.token_hex(32)}; locale=en-US',
		'DNT': '1',
		'origin': 'https://discord.com',
		'sec-fetch-dest': 'empty',
		'sec-fetch-mode': 'cors',
		'sec-fetch-site': 'same-origin',
		'referer': 'https://discord.com/channels/@me',
		'TE': 'Trailers',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9001 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36',
		'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDAxIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDIiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6ODMwNDAsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9',
    }
    return header
        

def change_password(email, token, oldPass, newPass):

    headers = getheaders(token)
    
    payload = {
        'password': oldPass,
        'new_password': newPass,
    }

    r = requests.patch(f"https://discord.com/api/v9/users/@me", json=payload, headers=headers)

    newToken = r.json().get("token")
    
    if(newToken):
        emailpass = f"{email}:{oldPass}:{token}"
        print(f'{Fore.BLUE}{Style.BRIGHT}[{Fore.RESET}{Fore.YELLOW}{Style.BRIGHT}JNX{Fore.RESET}{Fore.BLUE}{Style.BRIGHT}]{Fore.RESET} {Fore.GREEN}{Style.BRIGHT}Şifre Değiştirildi{Fore.RESET} ' + newToken)
        with open("./data/newpass.txt", "a") as x: x.write(f'{email}:{newPass}:{newToken}\n')
        with open("data/emailpass.txt", "r+") as io:
            tokens = io.readlines()
            io.seek(0)
            for line in tokens:
                if not (emailpass in line):
                    io.write(line)
                    io.truncate()
    else:
        print(f'{Fore.BLUE}{Style.BRIGHT}[{Fore.RESET}{Fore.YELLOW}{Style.BRIGHT}>{Fore.RESET}{Fore.BLUE}{Style.BRIGHT}]{Fore.RESET} {Fore.RED}{Style.BRIGHT}Şifre Değiştirilemedi{Fore.RESET} ' + token)
        emailpass = f"{email}:{oldPass}:{token}"
        with open("data/emailpass.txt", "r+") as io:
            tokens = io.readlines()
            io.seek(0)
            for line in tokens:
                if not (emailpass in line):
                    io.write(line)
                    io.truncate()

if __name__ == "__main__":

    os.system("title Token Password Changer")

    System.Size(150, 40)

    print('')
    print('')
    Write.Print("""
   ██████╗  █████╗ ███████╗███████╗     ██████╗██╗  ██╗ █████╗ ███╗   ██╗ ██████╗ ███████╗██████╗ 
   ██╔══██╗██╔══██╗██╔════╝██╔════╝    ██╔════╝██║  ██║██╔══██╗████╗  ██║██╔════╝ ██╔════╝██╔══██╗
   ██████╔╝███████║███████╗███████╗    ██║     ███████║███████║██╔██╗ ██║██║  ███╗█████╗  ██████╔╝
   ██╔═══╝ ██╔══██║╚════██║╚════██║    ██║     ██╔══██║██╔══██║██║╚██╗██║██║   ██║██╔══╝  ██╔══██╗
   ██║     ██║  ██║███████║███████║    ╚██████╗██║  ██║██║  ██║██║ ╚████║╚██████╔╝███████╗██║  ██║
   ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝         
    """, Colors.purple_to_blue, interval=0)
    print('')
    print('')

    emailpass =  open('./data/emailpass.txt','r').read().replace(" "," ").splitlines()
    for line in emailpass:
        email = line.split(':')[0]
        old = line.split(':')[1]
        token = line.split(':')[2]
        new = ""
        if config['newPass'] == "random":
            new = randomPassword(config['newPassLength'])
        else:
            new = config['newPass']
            
        change_password(email, token, old, new)