import requests
from bs4 import BeautifulSoup
import os
import json

# URL der Patch Notes Seite
url = "https://robertsspaceindustries.com/spectrum/community/SC/forum/190048"

# Discord Webhook URL aus den Umgebungsvariablen lesen
discord_webhook_url = os.getenv('DISCORD_WEBHOOK_URL')

# Funktion zum Abrufen und Parsen der Webseite
def fetch_patch_notes():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Patch Notes extrahieren (angepasst an die Struktur der Seite)
    patch_notes_section = soup.find('section', class_="thread-list")
    patch_notes = patch_notes_section.find_all('a', class_="thread-title")

    if patch_notes:
        latest_patch_note = patch_notes[0].get_text().strip()
        return latest_patch_note
    return None

# Funktion zum Senden der Nachricht an Discord
def send_to_discord(message):
    data = {
        "content": f"Neuer Patch Note: {message}"
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(discord_webhook_url, data=json.dumps(data), headers=headers)
    if response.status_code == 204:
        print("Nachricht erfolgreich gesendet.")
    else:
        print(f"Fehler beim Senden der Nachricht: {response.status_code}")

# Hauptlogik
def main():
    latest_patch_note = fetch_patch_notes()
    if latest_patch_note:
        send_to_discord(latest_patch_note)
    else:
        print("Keine neuen Patch Notes gefunden.")

if __name__ == "__main__":
    main()