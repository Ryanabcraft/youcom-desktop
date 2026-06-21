"""
browser_launcher.py — Cross-platform browser detector & launcher

Detects installed browsers on Windows, Linux, and macOS,
and launches a given URL in `--app` (distraction-free) mode.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

BROWSERS_WIN = [
    # Chrome
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    os.path.expandvars(r"%PROGRAMFILES%\Google\Chrome\Application\chrome.exe"),
    os.path.expandvars(r"%PROGRAMFILES(X86)%\Google\Chrome\Application\chrome.exe"),
    # Chrome Canary
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome SxS\Application\chrome.exe"),
    # Chrome Beta
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome Beta\Application\chrome.exe"),
    # Chrome Dev
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome Dev\Application\chrome.exe"),
    # Edge
    os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe"),
    os.path.expandvars(r"%PROGRAMFILES%\Microsoft\Edge\Application\msedge.exe"),
    os.path.expandvars(r"%PROGRAMFILES(X86)%\Microsoft\Edge\Application\msedge.exe"),
    # Edge Beta
    os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge Beta\Application\msedge.exe"),
    # Edge Dev
    os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge Dev\Application\msedge.exe"),
    # Brave
    os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\Application\brave.exe"),
    os.path.expandvars(r"%PROGRAMFILES%\BraveSoftware\Brave-Browser\Application\brave.exe"),
    os.path.expandvars(r"%PROGRAMFILES(X86)%\BraveSoftware\Brave-Browser\Application\brave.exe"),
    # Brave Beta
    os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser-Beta\Application\brave.exe"),
    # Brave Nightly
    os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser-Nightly\Application\brave.exe"),
    # Opera
    os.path.expandvars(r"%PROGRAMFILES%\Opera\launcher.exe"),
    os.path.expandvars(r"%PROGRAMFILES(X86)%\Opera\launcher.exe"),
    # Opera GX
    os.path.expandvars(r"%LOCALAPPDATA%\Programs\Opera GX\launcher.exe"),
    # Vivaldi
    os.path.expandvars(r"%LOCALAPPDATA%\Vivaldi\Application\vivaldi.exe"),
    os.path.expandvars(r"%PROGRAMFILES%\Vivaldi\Application\vivaldi.exe"),
    # Chromium
    os.path.expandvars(r"%LOCALAPPDATA%\Chromium\Application\chrome.exe"),
    os.path.expandvars(r"%PROGRAMFILES%\Chromium\Application\chrome.exe"),
    # Yandex
    os.path.expandvars(r"%LOCALAPPDATA%\Yandex\YandexBrowser\Application\browser.exe"),
    os.path.expandvars(r"%PROGRAMFILES%\Yandex\YandexBrowser\Application\browser.exe"),
    # Firefox
    os.path.expandvars(r"%PROGRAMFILES%\Mozilla Firefox\firefox.exe"),
    os.path.expandvars(r"%PROGRAMFILES(X86)%\Mozilla Firefox\firefox.exe"),
    # Epic
    os.path.expandvars(r"%LOCALAPPDATA%\Epic Privacy Browser\Application\epic.exe"),
    # Comodo Dragon
    os.path.expandvars(r"%PROGRAMFILES%\Comodo\Dragon\browser.exe"),
    # Slimjet
    os.path.expandvars(r"%PROGRAMFILES%\Slimjet\slimjet.exe"),
    # Coc Coc
    os.path.expandvars(r"%LOCALAPPDATA%\CocCoc\Browser\Application\browser.exe"),
]

BROWSERS_LINUX = [
    "google-chrome",
    "google-chrome-stable",
    "google-chrome-beta",
    "google-chrome-unstable",
    "chromium",
    "chromium-browser",
    "brave-browser",
    "brave-browser-beta",
    "brave-browser-nightly",
    "microsoft-edge",
    "microsoft-edge-stable",
    "microsoft-edge-beta",
    "microsoft-edge-dev",
    "opera",
    "vivaldi",
    "firefox",
    "firefox-esr",
    "epiphany",
    "gnome-web",
    "falkon",
    "midori",
]

BROWSERS_MAC = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
    "/Applications/Google Chrome Beta.app/Contents/MacOS/Google Chrome Beta",
    "/Applications/Google Chrome Dev.app/Contents/MacOS/Google Chrome Dev",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Microsoft Edge Beta.app/Contents/MacOS/Microsoft Edge Beta",
    "/Applications/Microsoft Edge Dev.app/Contents/MacOS/Microsoft Edge Dev",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "/Applications/Brave Browser Beta.app/Contents/MacOS/Brave Browser Beta",
    "/Applications/Brave Browser Nightly.app/Contents/MacOS/Brave Browser Nightly",
    "/Applications/Opera.app/Contents/MacOS/Opera",
    "/Applications/Vivaldi.app/Contents/MacOS/Vivaldi",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Firefox.app/Contents/MacOS/firefox",
    "/Applications/Firefox Developer Edition.app/Contents/MacOS/firefox",
    "/Applications/Firefox Nightly.app/Contents/MacOS/firefox",
    "/Applications/Safari.app/Contents/MacOS/Safari",
]

FIREFOX_BINARIES_LINUX = ["firefox", "firefox-esr"]


def _is_firefox(browser_path):
    name = os.path.basename(browser_path).lower()
    return "firefox" in name or "firefox" in browser_path.lower()


def detect_browser():
    system = sys.platform

    if system == "win32":
        candidates = BROWSERS_WIN
    elif system == "darwin":
        candidates = BROWSERS_MAC
    elif system == "linux":
        candidates = BROWSERS_LINUX
    else:
        return None

    for candidate in candidates:
        if system == "linux":
            found = shutil.which(candidate)
            if found:
                return found
        else:
            path = os.path.expandvars(candidate) if "%" in candidate else candidate
            if os.path.isfile(path):
                return path

    return None


def launch_url(url, browser_path=None):
    if not browser_path:
        browser_path = detect_browser()

    if not browser_path:
        return False, "Nenhum navegador encontrado."

    is_firefox = _is_firefox(browser_path)
    system = sys.platform

    try:
        if is_firefox:
            if system == "darwin":
                args = ["open", "-a", browser_path, url]
            else:
                args = [browser_path, "--new-window", url]
        else:
            args = [browser_path, "--app=" + url, "--new-window", "--no-first-run", "--force-dark-mode"]

        subprocess.Popen(args)
        return True, None
    except Exception as e:
        return False, str(e)


def main():
    """CLI usage: python browser_launcher.py <url>"""
    url = sys.argv[1] if len(sys.argv) > 1 else "https://www.tiktok.com"
    browser = detect_browser()

    if browser:
        name = os.path.basename(browser)
        print(f"Navegador encontrado: {name}")
    else:
        print("Nenhum navegador encontrado.")
        sys.exit(1)

    ok, err = launch_url(url, browser)
    if not ok:
        print(f"Erro: {err}")
        sys.exit(1)

if __name__ == "__main__":
    main()
