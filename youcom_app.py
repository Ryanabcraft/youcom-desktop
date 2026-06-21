#!/usr/bin/env python3
"""You.com Desktop — abre You.com no navegador em modo app."""
from browser_launcher import detect_browser, launch_url
import sys
import json
import os
import webbrowser
from urllib.request import urlopen
from urllib.error import URLError

URL = "https://you.com"
VERSION = "1.0.0"
REPO = "Ryanabcraft/youcom-desktop"

def check_update():
    try:
        req = urlopen(f"https://api.github.com/repos/{REPO}/releases/latest", timeout=5)
        data = json.loads(req.read().decode())
        latest = data.get("tag_name", "").lstrip("v")
        gh_url = data.get("html_url", "")
        if latest and latest != VERSION:
            return latest, gh_url
    except (URLError, json.JSONDecodeError, OSError):
        pass
    return None

def msgbox(title, text, buttons=0):
    if sys.platform == "win32":
        import ctypes
        return ctypes.windll.user32.MessageBoxW(0, text, title, buttons)
    print(f"{title}: {text}")
    return 0

def main():
    update = check_update()
    if update:
        new_ver, gh_url = update
        resp = msgbox(
            "Atualização disponível",
            f"You.com Desktop v{new_ver} disponível!\n\n"
            f"Sua versão: v{VERSION}\n\n"
            "Deseja baixar a nova versão?",
            4
        )
        if resp == 6:
            webbrowser.open(gh_url)
            return

    browser = detect_browser()
    if not browser:
        msg = "Nenhum navegador encontrado!\n\nInstale Chrome, Edge, Brave, Firefox, Opera ou Vivaldi."
        msgbox("You.com Desktop", msg)
        sys.exit(1)

    launch_url(URL, browser)

if __name__ == "__main__":
    main()
