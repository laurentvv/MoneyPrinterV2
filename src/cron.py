# EXÉCUTER CE N NOMBRE DE FOIS
import sys

from status import *
from cache import get_accounts
from config import get_verbose
from classes.Tts import TTS
from classes.Twitter import Twitter
from classes.YouTube import YouTube

def main():
    """Fonction principale pour publier du contenu sur Twitter ou téléverser des vidéos sur YouTube.

    Cette fonction détermine son fonctionnement en fonction des arguments de la ligne de commande :
    - Si le but est "twitter", elle initialise un compte Twitter et publie un message.
    - Si le but est "youtube", elle initialise un compte YouTube, génère une vidéo avec TTS et la téléverse.

    Arguments de la ligne de commande :
        sys.argv[1] : Une chaîne de caractères indiquant le but, soit "twitter", soit "youtube".
        sys.argv[2] : Une chaîne de caractères représentant l'UUID du compte.

    La fonction gère également la sortie verbeuse en fonction des paramètres de l'utilisateur et signale les succès ou les erreurs, le cas échéant.

    Args:
        None. La fonction utilise les arguments de la ligne de commande accessibles via sys.argv.

    Returns:
        None. La fonction effectue des opérations en fonction du but et de l'UUID du compte et ne renvoie aucune valeur.
    """
    purpose = str(sys.argv[1])
    account_id = str(sys.argv[2])

    verbose = get_verbose()

    if purpose == "twitter":
        accounts = get_accounts("twitter")

        if not account_id:
            error("L'UUID du compte ne peut pas être vide.")

        for acc in accounts:
            if acc["id"] == account_id:
                if verbose:
                    info("Initialisation de Twitter...")
                twitter = Twitter(
                    acc["id"],
                    acc["nickname"],
                    acc["firefox_profile"],
                    acc["topic"]
                )
                twitter.post()
                if verbose:
                    success("Publication terminée.")
                break
    elif purpose == "youtube":
        tts = TTS()

        accounts = get_accounts("youtube")

        if not account_id:
            error("L'UUID du compte ne peut pas être vide.")

        for acc in accounts:
            if acc["id"] == account_id:
                if verbose:
                    info("Initialisation de YouTube...")
                youtube = YouTube(
                    acc["id"],
                    acc["nickname"],
                    acc["firefox_profile"],
                    acc["niche"],
                    acc["language"]
                )
                youtube.generate_video(tts)
                youtube.upload_video()
                if verbose:
                    success("Short téléversé.")
                break
    else:
        error("But invalide, sortie...")
        sys.exit(1)

if __name__ == "__main__":
    main()
