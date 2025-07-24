import os
import random
import zipfile
import requests
import platform

from status import *
from config import *

def close_running_selenium_instances() -> None:
    """
    Ferme toutes les instances Selenium en cours d'exécution.

    Returns:
        None
    """
    try:
        info(" => Fermeture des instances Selenium en cours d'exécution...")

        # Tuer toutes les instances Firefox en cours d'exécution
        if platform.system() == "Windows":
            os.system("taskkill /f /im firefox.exe")
        else:
            os.system("pkill firefox")

        success(" => Instances Selenium en cours d'exécution fermées.")

    except Exception as e:
        error(f"Erreur lors de la fermeture des instances Selenium en cours d'exécution: {str(e)}")

def build_url(youtube_video_id: str) -> str:
    """
    Construit l'URL de la vidéo YouTube.

    Args:
        youtube_video_id (str): L'ID de la vidéo YouTube.

    Returns:
        url (str): L'URL de la vidéo YouTube.
    """
    return f"https://www.youtube.com/watch?v={youtube_video_id}"

def rem_temp_files() -> None:
    """
    Supprime les fichiers temporaires dans le répertoire `.mp`.

    Returns:
        None
    """
    # Chemin vers le répertoire `.mp`
    mp_dir = os.path.join(ROOT_DIR, ".mp")

    files = os.listdir(mp_dir)

    for file in files:
        if not file.endswith(".json"):
            os.remove(os.path.join(mp_dir, file))

def fetch_songs() -> None:
    """
    Télécharge des chansons dans le répertoire songs/ à utiliser avec les vidéos générées.

    Returns:
        None
    """
    try:
        info(f" => Récupération des chansons...")

        files_dir = os.path.join(ROOT_DIR, "Songs")
        if not os.path.exists(files_dir):
            os.mkdir(files_dir)
            if get_verbose():
                info(f" => Répertoire créé: {files_dir}")
        else:
            # Ignorer si les chansons sont déjà téléchargées
            return

        # Télécharger les chansons
        response = requests.get(get_zip_url() or "https://filebin.net/bb9ewdtckolsf3sg/drive-download-20240209T180019Z-001.zip")

        # Enregistrer le fichier zip
        with open(os.path.join(files_dir, "songs.zip"), "wb") as file:
            file.write(response.content)

        # Décompresser le fichier
        with zipfile.ZipFile(os.path.join(files_dir, "songs.zip"), "r") as file:
            file.extractall(files_dir)

        # Supprimer le fichier zip
        os.remove(os.path.join(files_dir, "songs.zip"))

        success(" => Chansons téléchargées dans ../Songs.")

    except Exception as e:
        error(f"Erreur lors de la récupération des chansons: {str(e)}")

def choose_random_song() -> str:
    """
    Choisit une chanson au hasard dans le répertoire songs/.

    Returns:
        str: Le chemin vers la chanson choisie.
    """
    try:
        songs = os.listdir(os.path.join(ROOT_DIR, "Songs"))
        song = random.choice(songs)
        success(f" => Chanson choisie: {song}")
        return os.path.join(ROOT_DIR, "Songs", song)
    except Exception as e:
        error(f"Erreur lors du choix d'une chanson au hasard: {str(e)}")
