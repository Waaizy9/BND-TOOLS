"""Built-in dashboard tools."""
import os, sys, time, json, random, secrets, string, webbrowser
import urllib.request, urllib.error

from . import constants as C
from .void_common import (
    ansi_hex as _ansi, console, error_box as _error_box, open_premium_links,
    panel as _panel, pause as _pause, success_box as _success_box,
)
from .runner import run, run_nuker
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.padding import Padding
from rich import box

import re as _re
import urllib.parse as _urlparse

sp = " "
_VOID_DIR = C.VOID_DIR
VERSION = C.VERSION
GITHUB = C.GITHUB
DISCORD = C.DISCORD
CHANGELOG = C.CHANGELOG

_IP_RE = _re.compile(r'^[0-9a-fA-F.:]+$')
_DOMAIN_RE = _re.compile(r'^[a-zA-Z0-9]([a-zA-Z0-9\-]*[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]*[a-zA-Z0-9])?)*$')
_USERNAME_RE = _re.compile(r'^[a-zA-Z0-9._\-]+$')

# Farben direkt definieren (nicht aus C importieren)
C_BLOOD = "\033[91m"
C_MID = "\033[37m"
C_NEON = "\033[96m"
C_WHITE = "\033[97m"
C_SILVER = "\033[38;2;192;192;192m"
C_DIM = "\033[2m"
C_GOLD = "\033[38;2;255;215;0m"
C_GOLD2 = "\033[38;2;255;215;0m"


def star():
    import time
    _panel("PREMIUM ONLY", "Feature reserved for BND PREMIUM members.")
    console.print(Panel(
        Text.from_markup(
            f"[{C_SILVER}]Shop · Discord\n"
            f"[{C_GOLD2}]{C.SHOP}[/]\n"
            f"[{C_GOLD2}]{C.DISCORD}[/]"
        ), border_style=C_GOLD, box=box.ROUNDED, padding=(1, 2)))
    open_premium_links()
    time.sleep(1.5)


def tool_vpn_detector():
    import urllib.request, json
    _panel("VPN DETECTOR", "Detects VPN · Proxy · Tor for an IP")
    ip = input(f"{_ansi(C_MID)}  IP address >> \033[0m").strip()
    if not ip: return
    if not _IP_RE.match(ip) or len(ip) > 45:
        console.print(f"[{C_NEON} bold]  [!] Invalid IP address format")
        input(f"\033[38;2;136;0;0m  press enter...\033[0m")
        return
    console.print(Text.from_markup(f"[{C_NEON} bold] ┌── VPN Check : {ip}"))
    
    try:
        url = f"https://proxycheck.io/v2/{_urlparse.quote(ip, safe='')}?vpn=1&asn=1"
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            
            if data.get("status") != "ok":
                console.print(f"[{C_NEON} bold]  [!] Error: {data.get('message', 'Unknown error')}")
                return
            
            res = data.get(ip, {})
            is_proxy = res.get("proxy", "no") == "yes"
            p_color = C_NEON if is_proxy else "#00FF00"
            
            table = Table(box=box.MINIMAL_DOUBLE_HEAD, border_style=C_BLOOD, show_header=False)
            table.add_row(f"[{C_SILVER}]IP Address", f"[{C_WHITE}]{ip}")
            table.add_row(f"[{C_SILVER}]Proxy/VPN", f"[{p_color} bold]{res.get('proxy', 'no').upper()}")
            table.add_row(f"[{C_SILVER}]Type", f"[{C_WHITE}]{res.get('type', 'N/A')}")
            table.add_row(f"[{C_SILVER}]Provider", f"[{C_WHITE}]{res.get('provider', 'N/A')}")
            table.add_row(f"[{C_SILVER}]ASN", f"[{C_WHITE}]{res.get('asn', 'N/A')}")
            table.add_row(f"[{C_SILVER}]Country", f"[{C_WHITE}]{res.get('country', 'N/A')} ({res.get('isocode', '??')})")
            
            console.print(Padding(Panel(table, title=f"[{C_GOLD} bold]Results[/]", border_style=C_BLOOD), (1, 2)))
            
    except Exception as e:
        console.print(f"[{C_NEON} bold]  [!] Network Error: {e}")
    
    console.print(); input(f"\033[38;2;136;0;0m  press enter...\033[0m")

def tool_rar_premium():
    _panel("RAR CRACKER [PREMIUM]", "Feature reserved for Premium members.")
    console.print(f"\n[{C_GOLD} bold]  * VIP ACCESS REQUIRED\n[{C_WHITE}]  Shop · Discord\n[{C_GOLD2}]{C.SHOP}[/]\n[{C_GOLD2}]{C.DISCORD}[/]")
    open_premium_links()
    console.print(); input(f"\033[38;2;136;0;0m  press enter to return...\033[0m")

def tool_username_hunter():
    _panel("USERNAME HUNTER", "Search username on 12 platforms")
    u = input(f"{_ansi(C_MID)}  username >> \033[0m").strip()
    if not u: return
    if not _USERNAME_RE.match(u) or len(u) > 64:
        console.print(f"[{C_NEON} bold]  [!] Invalid username (alphanumeric, dots, hyphens, underscores only)")
        input(f"\033[38;2;136;0;0m  press enter...\033[0m")
        return
    console.print(Text.from_markup(f"[{C_NEON} bold] ┌── Results for : {u}"))
    _open_links([
        ("GitHub",    f"https://github.com/{u}"),
        ("Twitter/X", f"https://x.com/{u}"),
        ("Instagram", f"https://instagram.com/{u}"),
        ("TikTok",    f"https://tiktok.com/@{u}"),
        ("Reddit",    f"https://reddit.com/u/{u}"),
        ("Twitch",    f"https://twitch.tv/{u}"),
        ("YouTube",   f"https://youtube.com/@{u}"),
        ("Steam",     f"https://steamcommunity.com/id/{u}"),
        ("Snapchat",  f"https://snapchat.com/add/{u}"),
        ("Pinterest", f"https://pinterest.com/{u}"),
        ("Medium",    f"https://medium.com/@{u}"),
        ("Telegram",  f"https://t.me/{u}"),
    ])

def tool_domain_intel():
    _panel("DOMAIN INTEL", "WHOIS · DNS · SSL · Shodan · VirusTotal")
    d = input(f"{_ansi(C_MID)}  domain (ex: google.com) >> \033[0m").strip()
    if not d: return
    if not _DOMAIN_RE.match(d) or len(d) > 253:
        console.print(f"[{C_NEON} bold]  [!] Invalid domain format")
        input(f"\033[38;2;136;0;0m  press enter...\033[0m")
        return
    console.print(Text.from_markup(f"[{C_NEON} bold] ┌── Intel for : {d}"))
    _open_links([
        ("WHOIS",       f"https://who.is/whois/{d}"),
        ("DNS Lookup",  f"https://dnschecker.org/#A/{d}"),
        ("Subdomains",  f"https://subdomainfinder.c99.nl/?domain={d}"),
        ("SSL Cert",    f"https://crt.sh/?q={d}"),
        ("VirusTotal",  f"https://virustotal.com/gui/domain/{d}"),
        ("Shodan",      f"https://shodan.io/search?query=hostname%3A{d}"),
        ("URLScan",     f"https://urlscan.io/search/#domain%3A{d}"),
    ])

def tool_social_scraper():
    _panel("SOCIAL SCRAPER", "Public profile scraping tools")
    console.print(Text.from_markup(f"[{C_NEON} bold] ┌── Social Scraper Tools"))
    _open_links([
        ("Instagram",    "https://imginn.com/"),
        ("TikTok",       "https://exolyt.com/"),
        ("Facebook ID",  "https://lookup-id.com/"),
        ("LinkedIn",     "https://osint.support/"),
        ("Social Search","https://socialsearcher.com/"),
        ("Sherlock",     "https://sherlock-project.github.io/"),
    ])

def tool_sms_bomber():
    _panel("SMS BOMBER", "Web-based SMS flood platforms")
    console.print(Text.from_markup(f"[{C_NEON} bold] ┌── SMS Services"))
    _open_links([
        ("SMS24",        "https://sms24.me/"),
        ("SMSPool",      "https://smspool.net/"),
        ("TextBelt",     "https://textbelt.com/"),
        ("Receive-SMS",  "https://receive-sms.com/"),
        ("SMS Receive",  "https://smsreceivefree.com/"),
    ])

def tool_token_checker():
    import urllib.request, json
    _panel("TOKEN CHECKER", "Check Discord token validity")
    token = input(f"{_ansi(C_MID)}  Discord token >> \033[0m").strip()
    if not token: return
    try:
        req = urllib.request.Request(
            "https://discord.com/api/v9/users/@me",
            headers={"Authorization": token}
        )
        with urllib.request.urlopen(req, timeout=5) as r:
            d = json.loads(r.read())
        console.print(Panel(
            Text.from_markup(
                f"[{C_GOLD} bold]* TOKEN VALID *\n\n"
                f"[{C_SILVER}]User   : [{C_WHITE} bold]{d.get('username','?')}#{d.get('discriminator','0')}\n"
                f"[{C_SILVER}]ID     : [{C_WHITE}]{d.get('id','?')}\n"
                f"[{C_SILVER}]Email  : [{C_WHITE}]{d.get('email','hidden')}\n"
                f"[{C_SILVER}]Nitro  : [{C_WHITE}]{'Yes' if d.get('premium_type') else 'No'}\n"
                f"[{C_SILVER}]Phone  : [{C_WHITE}]{'Yes' if d.get('phone') else 'No'}"
            ),
            border_style=C_GOLD, box=box.DOUBLE_EDGE, padding=(0, 3)
        ))
    except Exception:
        console.print(f"\n[{C_NEON} bold]  [!] INVALID TOKEN or network error")
    console.print(); input(f"\033[38;2;136;0;0m  press enter...\033[0m")

def _check_discord_token(token):
    import urllib.request, urllib.error
    token = token.strip()
    if not token:
        return False, None
    try:
        req = urllib.request.Request(
            "https://discord.com/api/v9/users/@me",
            headers={"Authorization": token, "User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            return True, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return False, {"status": e.code}
    except Exception as ex:
        return False, {"error": str(ex)}

def _discord_user_tag(d):
    user = d.get("username", "?")
    disc = d.get("discriminator", "0")
    if disc and disc != "0":
        return f"{user}#{disc}"
    return user

def tool_token_checker_pro():
    _panel("TOKEN CHECKER PRO", "Mass check multiple Discord tokens")
    console.print(Text.from_markup(
        f"[{C_SILVER}]Paste your tokens (one per line), then empty line.\n"
        f"Or enter [bold]file[/] + path to .txt[/]"
    ))
    lines, raw = [], input(f"{_ansi(C_MID)}  >> \033[0m").strip()
    if raw.lower() == "file":
        fp = input(f"{_ansi(C_MID)}  .txt file >> \033[0m").strip().strip('"')
        if not fp or not os.path.isfile(fp):
            console.print(f"[{C_NEON} bold]  [!] file not found")
            time.sleep(2)
            return
        with open(fp, encoding="utf-8", errors="ignore") as f:
            lines = [l.strip() for l in f if l.strip()]
    else:
        if raw:
            lines.append(raw)
        while True:
            line = input().strip()
            if not line:
                break
            lines.append(line)
    tokens = list(dict.fromkeys(t for t in lines if t))
    if not tokens:
        console.print(f"[{C_NEON} bold]  [!] no tokens")
        time.sleep(2)
        return

    console.print(Text.from_markup(f"\n[{C_NEON} bold] ┌── {len(tokens)} token(s) checking...\n"))
    table = Table(box=box.MINIMAL_DOUBLE_HEAD, border_style=C_BLOOD, show_header=True)
    table.add_column("#", style=C_DIM, width=4)
    table.add_column("Status", width=10)
    table.add_column("User", style=C_WHITE)
    table.add_column("ID", style=C_SILVER)
    table.add_column("Nitro", width=6)
    table.add_column("Phone", width=6)
    table.add_column("Token", style=C_DIM, max_width=28)

    valid, invalid = [], []
    for i, tok in enumerate(tokens, 1):
        ok, data = _check_discord_token(tok)
        mask = tok[:18] + "..." if len(tok) > 21 else tok
        if ok and data:
            tag = _discord_user_tag(data)
            nitro = "Yes" if data.get("premium_type") else "No"
            phone = "Yes" if data.get("phone") else "No"
            table.add_row(str(i), f"[#00FF00 bold]VALID[/]", tag, str(data.get("id", "?")), nitro, phone, mask)
            valid.append({"token": tok, "user": tag, "id": data.get("id"), "data": data})
        else:
            err = data.get("status", "?") if isinstance(data, dict) else "err"
            table.add_row(str(i), f"[{C_NEON} bold]INVALID[/]", "-", "-", "-", "-", f"{mask} ({err})")
            invalid.append(tok)
        time.sleep(0.35)

    console.print(Padding(Panel(table, title=f"[{C_GOLD} bold]Results[/]", border_style=C_BLOOD), (1, 1)))
    console.print(Text.from_markup(
        f"\n[{C_SILVER}]valid   [{C_GOLD} bold]{len(valid)}[/]   "
        f"invalid [{C_NEON} bold]{len(invalid)}[/]   total {len(tokens)}"
    ))
    if valid:
        save = input(f"\n{_ansi(C_MID)}  save valid tokens? (yes/no) >> \033[0m").strip().lower()
        if save == "yes":
            out = os.path.join(_VOID_DIR, "data", "tokens-valid.txt")
            os.makedirs(os.path.dirname(out), exist_ok=True)
            with open(out, "w", encoding="utf-8") as f:
                for v in valid:
                    masked = v['token'][:8] + "***" + v['token'][-4:] if len(v['token']) > 12 else "***"
                    f.write(f"{masked}  |  {v['user']}  |  {v['id']}\n")
            console.print(f"[{C_GOLD} bold]  * saved (tokens masked)  {out}")
    console.print(); input(f"\033[38;2;136;0;0m  press enter...\033[0m")

def tool_changelog():
    _panel("CHANGELOG", f"BND-TOOLS v{VERSION}")
    console.print(Panel(C.CHANGELOG, border_style=C_GOLD, padding=(1, 2)))
    console.print(); input(f"\033[38;2;136;0;0m  press enter...\033[0m")

def tool_credits():
    _panel("CREDITS", f"BND-TOOLS · by {C.AUTHOR}")
    console.print(Panel(
        Text.from_markup(
            f"[{C_GOLD} bold]BND-TOOLS v{VERSION}[/]\n\n"
            f"[{C_WHITE}]Developer  : [bold]{C.AUTHOR}[/]\n"
            f"[{C_SILVER}]Discord    : {C.DISCORD}\n"
            f"[{C_SILVER}]Shop       : {C.SHOP}\n"
            f"[{C_SILVER}]GitHub     : {C.GITHUB}[/]"
        ), border_style=C_BLOOD, padding=(1, 3)))
    console.print(); input(f"\033[38;2;136;0;0m  press enter...\033[0m")

def tool_premium_shop():
    _panel("PREMIUM SHOP", "Buy BND PREMIUM")
    console.print(Text.from_markup(
        f"\n[{C_GOLD} bold]  * BND PREMIUM\n"
        f"[{C_WHITE}]  Official shop · Discord support [bold]{C.AUTHOR}[/]\n"
        f"[{C_GOLD2}]{C.SHOP}[/]\n"
        f"[{C_DIM}]{C.DISCORD}[/]"
    ))
    open_premium_links()
    console.print(); input(f"\033[38;2;136;0;0m  press enter...\033[0m")

def tool_version_info():
    _panel("VERSION", "BND-TOOLS system info")
    console.print(Panel(
        Text.from_markup(
            f"[{C_WHITE}]Version    : [bold {C_GOLD}]{VERSION}[/]\n"
            f"[{C_WHITE}]Edition    : PRIME\n"
            f"[{C_WHITE}]Python     : {sys.version.split()[0]}\n"
            f"[{C_WHITE}]Platform   : {sys.platform}"
        ), border_style=C_GOLD, padding=(1, 2)))
    console.print(); input(f"\033[38;2;136;0;0m  press enter...\033[0m")

def tool_patch_notes():
    tool_changelog()


def tool_hash_cracker():
    _panel("HASH CRACKER", "Crack MD5 · SHA1 · SHA256 via online lookup")
    h = input(f"{_ansi(C_MID)}  hash >> \033[0m").strip()
    if not h: return
    console.print(Text.from_markup(f"[{C_NEON} bold] ┌── Hash : {h[:40]}{'...' if len(h)>40 else ''}"))
    _open_links([
        ("CrackStation", "https://crackstation.net/"),
        ("HashKiller",   "https://hashkiller.io/listmanager"),
        ("MD5Decrypt",   "https://md5decrypt.net/"),
        ("Hashes.com",   "https://hashes.com/en/decrypt/hash"),
    ])


def tool_password_gen():
    _panel("PASSWORD GENERATOR", "Generate ultra-secure passwords")
    try: length = int(input(f"{_ansi(C_MID)}  length (default 20) >> \033[0m").strip() or "20")
    except ValueError: length = 20
    charset = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    console.print(); console.print(Text.from_markup(f"[{C_NEON} bold] ┌── 8 passwords  ·  length {length}"))
    for i in range(8):
        pwd = ''.join(secrets.choice(charset) for _ in range(length))
        t = Text()
        t.append(f" │   [{i+1:02d}] ", style=C_BLOOD)
        t.append(pwd, style=f"{C_WHITE} bold")
        console.print(t)
    console.print(); input(f"\033[38;2;136;0;0m  press enter...\033[0m")


def tool_temp_mail():
    _panel("TEMP MAIL", "Instant disposable email address")
    console.print(Text.from_markup(f"[{C_NEON} bold] ┌── Temp Mail Services"))
    _open_links([
        ("10MinuteMail",  "https://10minutemail.com/"),
        ("Guerrilla Mail","https://guerrillamail.com/"),
        ("TempMail",      "https://temp-mail.org/"),
        ("Mailnull",      "https://www.mailnull.com/"),
        ("Dispostable",   "https://dispostable.com/"),
        ("FakeMail",      "https://www.fakemail.net/"),
    ])


def tool_base64():
    _panel("BASE64", "Encode / Decode text")
    mode = input(f"{_ansi(C_MID)}  mode (encode/decode) >> \033[0m").strip().lower()
    txt = input(f"{_ansi(C_MID)}  text >> \033[0m").strip()
    if not txt: return
    import base64
    try:
        if mode.startswith("d"):
            out = base64.b64decode(txt).decode("utf-8", errors="replace")
        else:
            out = base64.b64encode(txt.encode()).decode()
        console.print(Panel(out, border_style=C_GOLD, title="Result"))
    except Exception as e:
        console.print(f"[{C_NEON} bold]  [!] {e}")
    console.print(); input(f"\033[38;2;136;0;0m  press enter...\033[0m")


def tool_qr_gen():
    _panel("QR GENERATOR", "Generate QR code via link")
    data = input(f"{_ansi(C_MID)}  text or URL >> \033[0m").strip()
    if not data: return
    import urllib.parse
    url = "https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=" + urllib.parse.quote(data)
    console.print(f"\n[{C_GOLD} bold]  QR URL:\n[{C_WHITE}]{url}")
    webbrowser.open(url)
    console.print(); input(f"\033[38;2;136;0;0m  press enter...\033[0m")


def tool_url_shortener():
    import urllib.request, urllib.parse
    _panel("URL SHORTENER", "Shorten URL (is.gd)")
    url = input(f"{_ansi(C_MID)}  long URL >> \033[0m").strip()
    if not url: return
    try:
        api = "https://is.gd/create.php?format=simple&url=" + urllib.parse.quote(url, safe="")
        with urllib.request.urlopen(api, timeout=10) as r:
            short = r.read().decode().strip()
        console.print(Panel(f"[bold white]{short}[/]", title="[gold]Short URL[/]", border_style=C_GOLD))
    except Exception as e:
        console.print(f"[{C_NEON} bold]  [!] {e}")
    console.print(); input(f"\033[38;2;136;0;0m  press enter...\033[0m")


def tool_json_fmt():
    _panel("JSON FORMATTER", "Pretty-print JSON")
    console.print(f"[{C_DIM}]  Paste JSON, empty line to finish[/]")
    lines, line = [], input()
    if line.strip():
        lines.append(line)
        while True:
            line = input()
            if not line.strip(): break
            lines.append(line)
    raw = "\n".join(lines).strip()
    if not raw: return
    try:
        obj = json.loads(raw)
        console.print(Panel(json.dumps(obj, indent=2, ensure_ascii=False), border_style=C_GOLD))
    except Exception as e:
        console.print(f"[{C_NEON} bold]  [!] Invalid JSON: {e}")
    console.print(); input(f"\033[38;2;136;0;0m  press enter...\033[0m")


def _open_links(items):
    for name, url in items:
        console.print(Text.from_markup(f"  │ [{C_WHITE}]{name:<12}[/]  [{C_GOLD2}]{url}[/]"))
    if input(f"\n{_ansi(C_MID)}  open in browser? (y/n) >> \033[0m").lower() in ("y", "yes", "j", "ja"):
        for _, url in items:
            webbrowser.open(url)