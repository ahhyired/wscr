import requests
from bs4 import BeautifulSoup, Comment
from urllib.parse import urljoin
from datetime import datetime
from art import *
from colorama import Fore
import validators
import os

print(Fore.GREEN)
tprint("WSCR", "rnd-xlarge")
print(Fore.WHITE)

def scrape_everything(url):
    if url == "q":
        return
    s = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Checking: If Url Valid | {s}")
    if validators.url(url):
        print("Url is valid. Starting The Search.")
    else:
        print("Please Input Valid Url.")
        print(f"\n[Programm Finished]")
        input("input to close")
        return

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return

    with open('scrape_results.txt', 'w') as file:
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            file.write(f"[+] Searched: {url} | {now}\n")
            
            # --- Find all links ---
            file.write(f"\n[+] Links (a) (at {now}):\n")
            links = soup.find_all('a', href=True)
            if links == "[]":
                file.write("Found none")
            for link in links:
                absolute_url = urljoin(url, link['href'])
                file.write(f"{absolute_url}\n")

            # --- Find all images ---
            file.write(f"\n[+] Images (img) (at {now}):\n")
            images = soup.find_all('img', src=True)
            if images == "[]":
                file.write("Found none")
            for img in images:
                img_url = urljoin(url, img['src'])
                file.write(f"{img_url}\n")

            # --- Find all CSS files ---
            file.write(f"\n[+] Stylesheets (CSS) (at {now}):\n")
            css_files = soup.find_all('link', rel="stylesheet")
            if css_files == "[]":
                file.write("Found none")
            for css in css_files:
                css_url = urljoin(url, css['href'])
                file.write(f"{css_url}\n")

            # --- Find all JavaScript files ---
            file.write(f"\n[+] JavaScript Files (.js) (at {now}):\n")
            scripts = soup.find_all('script', src=True)
            if scripts == "[]":
                file.write("Found none")
            for script in scripts:
                script_url = urljoin(url, script['src'])
                file.write(f"{script_url}\n")

            # --- Find all Audio files ---
            file.write(f"\n[+] Audio Files (audio, .mp3, .wav, .ogg) (at {now}):\n")
            audio_files = soup.find_all('audio', src=True)
            if audio_files == "[]":
                file.write("Found none")
            for audio in audio_files:
                audio_url = urljoin(url, audio['src'])
                file.write(f"{audio_url}\n")
            # Also check links with common audio file extensions
            for link in links:
                if any(link['href'].endswith(ext) for ext in ['.mp3', '.wav', '.ogg']):
                    absolute_url = urljoin(url, link['href'])
                    file.write(f"{absolute_url}\n")

            # --- Find robots.txt ---
            file.write(f"\n[+] Robots.txt Link (at {now}):\n")
            robots_url = urljoin(url, '/robots.txt')
            file.write(f"{robots_url}\n")

            # --- Find HTML comments ---
            file.write(f"\n[+] HTML Comments (at {now}):\n")
            comments = soup.find_all(string=lambda text: isinstance(text, Comment))
            if comments == "[]":
                file.write("Found none")
            for comment in comments:
                file.write(f"<!-- {comment} -->\n")

            # --- Find hidden input fields ---
            file.write(f"\n[+] Hidden Input Fields (at {now}):\n")
            hidden_inputs = soup.find_all('input', {'type': 'hidden'})
            if hidden_inputs == "[]":
                file.write("Found none")
            for hidden_input in hidden_inputs:
                file.write(f"{hidden_input}\n")

            # --- Find canonical link ---
            file.write(f"\n[+] Canonical Link (at {now}):\n")
            canonical = soup.find('link', rel='canonical')
            if canonical == "[]":
                file.write("Found none")
            if canonical and canonical.get('href'):
                canonical_url = urljoin(url, canonical['href'])
                file.write(f"{canonical_url}\n")

            # --- Find iFrames ---
            file.write(f"\n[+] iFrames (at {now}):\n")
            iframes = soup.find_all('iframe', src=True)
            if iframes == "[]":
                file.write("Found none")
            for iframe in iframes:
                iframe_url = urljoin(url, iframe['src'])
                file.write(f"{iframe_url}\n")

            # --- Find other potential files linked with 'link' tag (favicon, etc.) ---
            file.write(f"\n[+] Other Linked Files (via <link> tag) (at {now}):\n")
            linked_files = soup.find_all('link', href=True)
            if linked_files == "[]":
                file.write("Found none")
            for file_link in linked_files:
                linked_file_url = urljoin(url, file_link['href'])
                file.write(f"{linked_file_url}\n")
                
            fin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"\n[+] Finished at {fin}") 
            print(f"Finished. | {fin}")
            print(f"File saved at: {os.path.abspath('scrape_results.txt')}")
            print("\n[Programm Finished]")
            input("Enter to close")
        else:
            file.write(f"Failed to retrieve the webpage. Status code: {response.status_code}")

url_to_scrape = input("Enter Url: ")
scrape_everything(url_to_scrape)