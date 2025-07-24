import os
import sys
import json
import srt_equalizer

from termcolor import colored

ROOT_DIR = os.path.dirname(sys.path[0])

def assert_folder_structure() -> None:
    """
    S'assure que la structure de dossiers nécessaire est présente.

    Returns:
        None
    """
    # Créer le dossier .mp
    if not os.path.exists(os.path.join(ROOT_DIR, ".mp")):
        if get_verbose():
            print(colored(f"=> Création du dossier .mp à {os.path.join(ROOT_DIR, '.mp')}", "green"))
        os.makedirs(os.path.join(ROOT_DIR, ".mp"))

def get_first_time_running() -> bool:
    """
    Vérifie si le programme est exécuté pour la première fois en vérifiant si le dossier .mp existe.

    Returns:
        exists (bool): True si le programme est exécuté pour la première fois, False sinon
    """
    return not os.path.exists(os.path.join(ROOT_DIR, ".mp"))

def get_email_credentials() -> dict:
    """
    Obtient les informations d'identification de l'e-mail à partir du fichier de configuration.

    Returns:
        credentials (dict): Les informations d'identification de l'e-mail
    """
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["email"]

def get_verbose() -> bool:
    """
    Obtient le drapeau verbose à partir du fichier de configuration.

    Returns:
        verbose (bool): Le drapeau verbose
    """
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["verbose"]

def get_firefox_profile_path() -> str:
    """
    Obtient le chemin vers le profil Firefox.

    Returns:
        path (str): Le chemin vers le profil Firefox
    """
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["firefox_profile"]

def get_headless() -> bool:
    """
    Obtient le drapeau headless à partir du fichier de configuration.

    Returns:
        headless (bool): Le drapeau headless
    """
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["headless"]

def get_model() -> str:
    """
    Obtient le modèle à partir du fichier de configuration.

    Returns:
        model (str): Le modèle
    """
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["llm"]

def get_twitter_language() -> str:
    """
    Obtient la langue de Twitter à partir du fichier de configuration.

    Returns:
        language (str): La langue de Twitter
    """
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["twitter_language"]

def get_image_model() -> str:
    """
    Obtient le modèle d'image à partir du fichier de configuration.

    Returns:
        model (str): Le modèle d'image
    """
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["image_model"]

def get_threads() -> int:
    """
    Obtient le nombre de threads à utiliser, par exemple lors de l'écriture d'un fichier avec MoviePy.

    Returns:
        threads (int): Le nombre de threads
    """
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["threads"]
    
def get_image_prompt_llm() -> str:
    """
    Obtient le prompt d'image pour le LLM à partir du fichier de configuration.

    Returns:
        prompt (str): Le prompt d'image
    """
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["image_prompt_llm"]

def get_zip_url() -> str:
    """
    Obtient l'URL du fichier zip contenant les chansons.

    Returns:
        url (str): L'URL du fichier zip
    """
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["zip_url"]

def get_is_for_kids() -> bool:
    """
    Obtient le drapeau "is for kids" à partir du fichier de configuration.

    Returns:
        is_for_kids (bool): Le drapeau "is for kids"
    """
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["is_for_kids"]

def get_google_maps_scraper_zip_url() -> str:
    """
    Obtient l'URL du fichier zip contenant le scraper de Google Maps.

    Returns:
        url (str): L'URL du fichier zip
    """
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["google_maps_scraper"]

def get_google_maps_scraper_niche() -> str:
    """
    Obtient la niche pour le scraper de Google Maps.

    Returns:
        niche (str): La niche
    """
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["google_maps_scraper_niche"]

def get_scraper_timeout() -> int:
    """
    Obtient le timeout pour le scraper.

    Returns:
        timeout (int): Le timeout
    """
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["scraper_timeout"] or 300

def get_outreach_message_subject() -> str:
    """
    Obtient le sujet du message de prospection.

    Returns:
        subject (str): Le sujet du message de prospection
    """
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["outreach_message_subject"]
    
def get_outreach_message_body_file() -> str:
    """
    Obtient le fichier du corps du message de prospection.

    Returns:
        file (str): Le fichier du corps du message de prospection
    """
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["outreach_message_body_file"]

def get_assemblyai_api_key() -> str:
    """
    Obtient la clé API AssemblyAI.

    Returns:
        key (str): La clé API AssemblyAI
    """
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["assembly_ai_api_key"]
    
def equalize_subtitles(srt_path: str, max_chars: int = 10) -> None:
    """
    Égalise les sous-titres dans un fichier SRT.

    Args:
        srt_path (str): Le chemin vers le fichier SRT
        max_chars (int): Le nombre maximum de caractères dans un sous-titre

    Returns:
        None
    """
    srt_equalizer.equalize_srt_file(srt_path, srt_path, max_chars)
    
def get_font() -> str:
    """
    Obtient la police à partir du fichier de configuration.

    Returns:
        font (str): La police
    """
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["font"]

def get_fonts_dir() -> str:
    """
    Obtient le répertoire des polices.

    Returns:
        dir (str): Le répertoire des polices
    """
    return os.path.join(ROOT_DIR, "fonts")

def get_imagemagick_path() -> str:
    """
    Obtient le chemin vers ImageMagick.

    Returns:
        path (str): Le chemin vers ImageMagick
    """
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        return json.load(file)["imagemagick_path"]

def get_script_sentence_length() -> int:
    """
    Obtient la longueur de phrase forcée du script.
    S'il n'y a pas de longueur de phrase dans la configuration, retourne 4.

    Returns:
        length (int): Longueur de la phrase du script
    """
    with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
        config_json = json.load(file)
        if (config_json.get("script_sentence_length") is not None):
            return config_json["script_sentence_length"]
        else:
            return 4
