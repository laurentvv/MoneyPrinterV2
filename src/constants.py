"""
Ce fichier contient toutes les constantes utilisées dans le programme.
"""
import g4f

TWITTER_TEXTAREA_CLASS = "public-DraftStyleDefault-block public-DraftStyleDefault-ltr"
TWITTER_POST_BUTTON_XPATH = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/div[3]"

OPTIONS = [
    "Automatisation des YouTube Shorts",
    "Bot Twitter",
    "Marketing d'affiliation",
    "Prospection",
    "Quitter"
]

TWITTER_OPTIONS = [
    "Publier quelque chose",
    "Afficher toutes les publications",
    "Configurer une tâche CRON",
    "Quitter"
]

TWITTER_CRON_OPTIONS = [
    "Une fois par jour",
    "Deux fois par jour",
    "Trois fois par jour",
    "Quitter"
]

YOUTUBE_OPTIONS = [
    "Téléverser un Short",
    "Afficher tous les Shorts",
    "Configurer une tâche CRON",
    "Quitter"
]

YOUTUBE_CRON_OPTIONS = [
    "Une fois par jour",
    "Deux fois par jour",
    "Trois fois par jour",
    "Quitter"
]

# Section YouTube
YOUTUBE_TEXTBOX_ID = "textbox"
YOUTUBE_MADE_FOR_KIDS_NAME = "VIDEO_MADE_FOR_KIDS_MFK"
YOUTUBE_NOT_MADE_FOR_KIDS_NAME = "VIDEO_MADE_FOR_KIDS_NOT_MFK"
YOUTUBE_NEXT_BUTTON_ID = "next-button"
YOUTUBE_RADIO_BUTTON_XPATH = "//*[@id=\"radioLabel\"]"
YOUTUBE_DONE_BUTTON_ID = "done-button"

# Section Amazon (AFM)
AMAZON_PRODUCT_TITLE_ID = "productTitle"
AMAZON_FEATURE_BULLETS_ID = "feature-bullets"

def parse_model(model_name: str) -> any:
    """Récupère un objet modèle en fonction du nom de modèle fourni.

    Args:
        model_name (str): Le nom du modèle à récupérer. Les noms pris en charge sont
            "gpt4", "gpt35_turbo", "llama2_7b", "llama2_13b", "llama2_70b" et "mixtral_8x7b".

    Returns:
        any: L'objet modèle correspondant du module `g4f.models`. Si le nom du
        modèle n'est pas reconnu, la fonction renvoie par défaut le modèle "gpt35_turbo".
    """
    if model_name == "gpt4":
        return g4f.models.gpt_4
    elif model_name == "gpt35_turbo":
        return g4f.models.gpt_4o_mini
    elif model_name == "llama2_7b":
        return g4f.models.llama2_7b
    elif model_name == "llama2_13b":
        return g4f.models.llama2_13b
    elif model_name == "llama2_70b":
        return g4f.models.llama2_70b
    elif model_name == "mixtral_8x7b":
        return g4f.models.mixtral_8x7b
    else:
        # Le modèle par défaut est gpt3.5-turbo
        return g4f.models.gpt_4o_mini
