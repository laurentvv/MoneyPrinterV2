import schedule
import subprocess

from art import *
from cache import *
from utils import *
from config import *
from status import *
from uuid import uuid4
from constants import *
from classes.Tts import TTS
from termcolor import colored
from classes.Twitter import Twitter
from classes.YouTube import YouTube
from prettytable import PrettyTable
from classes.Outreach import Outreach
from classes.AFM import AffiliateMarketing

def main():
    """Point d'entrée principal de l'application, fournissant une interface pilotée par menu
    pour gérer les tâches YouTube, Twitter, de marketing d'affiliation et de prospection.

    Cette fonction permet aux utilisateurs de :
    1. Démarrer l'automatisation des YouTube Shorts pour gérer les comptes YouTube,
       générer et téléverser des vidéos, et configurer des tâches CRON.
    2. Démarrer un bot Twitter pour gérer les comptes Twitter, publier des tweets et
       planifier des publications à l'aide de tâches CRON.
    3. Gérer le marketing d'affiliation en créant des argumentaires et en les partageant via
       les comptes Twitter.
    4. Lancer un processus de prospection pour les tâches d'engagement et de promotion.
    5. Quitter l'application.

    La fonction demande en continu à l'utilisateur une entrée, la valide et
    exécute l'option sélectionnée jusqu'à ce que l'utilisateur choisisse de quitter.

    Args:
        None

    Returns:
        None
    """

    # Obtenir l'entrée de l'utilisateur
    valid_input = False
    while not valid_input:
        try:
            # Afficher les options à l'utilisateur
            info("\n============ OPTIONS ============", False)

            for idx, option in enumerate(OPTIONS):
                print(colored(f" {idx + 1}. {option}", "cyan"))

            info("=================================\n", False)
            user_input = input("Sélectionnez une option: ").strip()
            if user_input == '':
                print("\n" * 100)
                raise ValueError("L'entrée vide n'est pas autorisée.")
            user_input = int(user_input)
            valid_input = True
        except ValueError as e:
            print("\n" * 100)
            print(f"Entrée invalide: {e}")


    # Démarrer l'option sélectionnée
    if user_input == 1:
        info("Démarrage de l'automatisation des YouTube Shorts...")

        cached_accounts = get_accounts("youtube")

        if len(cached_accounts) == 0:
            warning("Aucun compte trouvé dans le cache. En créer un maintenant?")
            user_input = question("Oui/Non: ")

            if user_input.lower() == "yes":
                generated_uuid = str(uuid4())

                success(f" => ID généré: {generated_uuid}")
                nickname = question(" => Entrez un surnom pour ce compte: ")
                fp_profile = question(" => Entrez le chemin vers le profil Firefox: ")
                niche = question(" => Entrez la niche du compte: ")
                language = question(" => Entrez la langue du compte: ")
                
                # Ajouter les options de génération d'images
                info("\n============ GÉNÉRATION D'IMAGES ============", False)
                print(colored(" 1. G4F (SDXL Turbo)", "cyan"))
                print(colored(" 2. Cloudflare Worker", "cyan"))
                info("=======================================", False)
                print(colored("\nRecommandation: Si vous n'êtes pas sûr, sélectionnez G4F (Option 1) car il n'y a pas de configuration supplémentaire", "yellow"))
                info("=======================================\n", False)
                
                image_gen_choice = question(" => Sélectionnez la méthode de génération d'images (1/2): ")
                
                account_data = {
                    "id": generated_uuid,
                    "nickname": nickname,
                    "firefox_profile": fp_profile,
                    "niche": niche,
                    "language": language,
                    "use_g4f": image_gen_choice == "1",
                    "videos": []
                }
                
                if image_gen_choice == "2":
                    worker_url = question(" => Entrez l'URL de votre worker Cloudflare pour la génération d'images: ")
                    account_data["worker_url"] = worker_url

                add_account("youtube", account_data)

                success("Compte configuré avec succès!")
        else:
            table = PrettyTable()
            table.field_names = ["ID", "UUID", "Surnom", "Niche"]

            for account in cached_accounts:
                table.add_row([cached_accounts.index(account) + 1, colored(account["id"], "cyan"), colored(account["nickname"], "blue"), colored(account["niche"], "green")])

            print(table)

            user_input = question("Sélectionnez un compte pour commencer: ")

            selected_account = None

            for account in cached_accounts:
                if str(cached_accounts.index(account) + 1) == user_input:
                    selected_account = account

            if selected_account is None:
                error("Compte invalide sélectionné. Veuillez réessayer.", "red")
                main()
            else:
                youtube = YouTube(
                    selected_account["id"],
                    selected_account["nickname"],
                    selected_account["firefox_profile"],
                    selected_account["niche"],
                    selected_account["language"]
                )

                while True:
                    rem_temp_files()
                    info("\n============ OPTIONS ============", False)

                    for idx, youtube_option in enumerate(YOUTUBE_OPTIONS):
                        print(colored(f" {idx + 1}. {youtube_option}", "cyan"))

                    info("=================================\n", False)

                    # Obtenir l'entrée de l'utilisateur
                    user_input = int(question("Sélectionnez une option: "))
                    tts = TTS()

                    if user_input == 1:
                        youtube.generate_video(tts)
                        upload_to_yt = question("Voulez-vous téléverser cette vidéo sur YouTube? (Oui/Non): ")
                        if upload_to_yt.lower() == "yes":
                            youtube.upload_video()
                    elif user_input == 2:
                        videos = youtube.get_videos()

                        if len(videos) > 0:
                            videos_table = PrettyTable()
                            videos_table.field_names = ["ID", "Date", "Titre"]

                            for video in videos:
                                videos_table.add_row([
                                    videos.index(video) + 1,
                                    colored(video["date"], "blue"),
                                    colored(video["title"][:60] + "...", "green")
                                ])

                            print(videos_table)
                        else:
                            warning(" Aucune vidéo trouvée.")
                    elif user_input == 3:
                        info("À quelle fréquence voulez-vous téléverser?")

                        info("\n============ OPTIONS ============", False)
                        for idx, cron_option in enumerate(YOUTUBE_CRON_OPTIONS):
                            print(colored(f" {idx + 1}. {cron_option}", "cyan"))

                        info("=================================\n", False)

                        user_input = int(question("Sélectionnez une option: "))

                        cron_script_path = os.path.join(ROOT_DIR, "src", "cron.py")
                        command = f"python {cron_script_path} youtube {selected_account['id']}"

                        def job():
                            """Exécute une commande shell à l'aide de subprocess.run.

                            Cette fonction exécute une commande shell spécifiée à l'aide du module subprocess.
                            La commande à exécuter doit être définie dans la variable 'command'.

                            Args:
                                None

                            Returns:
                                None
                            """
                            subprocess.run(command)

                        if user_input == 1:
                            # Téléverser une fois
                            schedule.every(1).day.do(job)
                            success("Tâche CRON configurée.")
                        elif user_input == 2:
                            # Téléverser deux fois par jour
                            schedule.every().day.at("10:00").do(job)
                            schedule.every().day.at("16:00").do(job)
                            success("Tâche CRON configurée.")
                        else:
                            break
                    elif user_input == 4:
                        if get_verbose():
                            info(" => Remontée dans l'échelle des options...", False)
                        break
    elif user_input == 2:
        info("Démarrage du bot Twitter...")

        cached_accounts = get_accounts("twitter")

        if len(cached_accounts) == 0:
            warning("Aucun compte trouvé dans le cache. En créer un maintenant?")
            user_input = question("Oui/Non: ")

            if user_input.lower() == "yes":
                generated_uuid = str(uuid4())

                success(f" => ID généré: {generated_uuid}")
                nickname = question(" => Entrez un surnom pour ce compte: ")
                fp_profile = question(" => Entrez le chemin vers le profil Firefox: ")
                topic = question(" => Entrez le sujet du compte: ")

                add_account("twitter", {
                    "id": generated_uuid,
                    "nickname": nickname,
                    "firefox_profile": fp_profile,
                    "topic": topic,
                    "posts": []
                })
        else:
            table = PrettyTable()
            table.field_names = ["ID", "UUID", "Surnom", "Sujet du compte"]

            for account in cached_accounts:
                table.add_row([cached_accounts.index(account) + 1, colored(account["id"], "cyan"), colored(account["nickname"], "blue"), colored(account["topic"], "green")])

            print(table)

            user_input = question("Sélectionnez un compte pour commencer: ")

            selected_account = None

            for account in cached_accounts:
                if str(cached_accounts.index(account) + 1) == user_input:
                    selected_account = account

            if selected_account is None:
                error("Compte invalide sélectionné. Veuillez réessayer.", "red")
                main()
            else:
                twitter = Twitter(selected_account["id"], selected_account["nickname"], selected_account["firefox_profile"], selected_account["topic"])

                while True:
                    
                    info("\n============ OPTIONS ============", False)

                    for idx, twitter_option in enumerate(TWITTER_OPTIONS):
                        print(colored(f" {idx + 1}. {twitter_option}", "cyan"))

                    info("=================================\n", False)

                    # Obtenir l'entrée de l'utilisateur
                    user_input = int(question("Sélectionnez une option: "))

                    if user_input == 1:
                        twitter.post()
                    elif user_input == 2:
                        posts = twitter.get_posts()

                        posts_table = PrettyTable()

                        posts_table.field_names = ["ID", "Date", "Contenu"]

                        for post in posts:
                            posts_table.add_row([
                                posts.index(post) + 1,
                                colored(post["date"], "blue"),
                                colored(post["content"][:60] + "...", "green")
                            ])

                        print(posts_table)
                    elif user_input == 3:
                        info("À quelle fréquence voulez-vous publier?")

                        info("\n============ OPTIONS ============", False)
                        for idx, cron_option in enumerate(TWITTER_CRON_OPTIONS):
                            print(colored(f" {idx + 1}. {cron_option}", "cyan"))

                        info("=================================\n", False)

                        user_input = int(question("Sélectionnez une option: "))

                        cron_script_path = os.path.join(ROOT_DIR, "src", "cron.py")
                        command = f"python {cron_script_path} twitter {selected_account['id']}"

                        def job():
                            """Exécute une commande shell à l'aide de subprocess.run.

                            Cette fonction exécute une commande shell spécifiée à l'aide du module subprocess.
                            La commande à exécuter doit être définie dans la variable 'command'.

                            Args:
                                None

                            Returns:
                                None
                            """
                            subprocess.run(command)

                        if user_input == 1:
                            # Publier une fois par jour
                            schedule.every(1).day.do(job)
                            success("Tâche CRON configurée.")
                        elif user_input == 2:
                            # Publier deux fois par jour
                            schedule.every().day.at("10:00").do(job)
                            schedule.every().day.at("16:00").do(job)
                            success("Tâche CRON configurée.")
                        elif user_input == 3:
                            # Publier trois fois par jour
                            schedule.every().day.at("08:00").do(job)
                            schedule.every().day.at("12:00").do(job)
                            schedule.every().day.at("18:00").do(job)
                            success("Tâche CRON configurée.")
                        else:
                            break
                    elif user_input == 4:
                        if get_verbose():
                            info(" => Remontée dans l'échelle des options...", False)
                        break
    elif user_input == 3:
        info("Démarrage du marketing d'affiliation...")

        cached_products = get_products()

        if len(cached_products) == 0:
            warning("Aucun produit trouvé dans le cache. En créer un maintenant?")
            user_input = question("Oui/Non: ")

            if user_input.lower() == "yes":
                affiliate_link = question(" => Entrez le lien d'affiliation: ")
                twitter_uuid = question(" => Entrez l'UUID du compte Twitter: ")

                # Trouver le compte
                account = None
                for acc in get_accounts("twitter"):
                    if acc["id"] == twitter_uuid:
                        account = acc

                add_product({
                    "id": str(uuid4()),
                    "affiliate_link": affiliate_link,
                    "twitter_uuid": twitter_uuid
                })

                afm = AffiliateMarketing(affiliate_link, account["firefox_profile"], account["id"], account["nickname"], account["topic"])

                afm.generate_pitch()
                afm.share_pitch("twitter")
        else:
            table = PrettyTable()
            table.field_names = ["ID", "Lien d'affiliation", "UUID du compte Twitter"]

            for product in cached_products:
                table.add_row([cached_products.index(product) + 1, colored(product["affiliate_link"], "cyan"), colored(product["twitter_uuid"], "blue")])

            print(table)

            user_input = question("Sélectionnez un produit pour commencer: ")

            selected_product = None

            for product in cached_products:
                if str(cached_products.index(product) + 1) == user_input:
                    selected_product = product

            if selected_product is None:
                error("Produit invalide sélectionné. Veuillez réessayer.", "red")
                main()
            else:
                # Trouver le compte
                account = None
                for acc in get_accounts("twitter"):
                    if acc["id"] == selected_product["twitter_uuid"]:
                        account = acc

                afm = AffiliateMarketing(selected_product["affiliate_link"], account["firefox_profile"], account["id"], account["nickname"], account["topic"])

                afm.generate_pitch()
                afm.share_pitch("twitter")

    elif user_input == 4:
        info("Démarrage de la prospection...")

        outreach = Outreach()

        outreach.start()
    elif user_input == 5:
        if get_verbose():
            print(colored(" => Quitter...", "blue"))
        sys.exit(0)
    else:
        error("Option invalide sélectionnée. Veuillez réessayer.", "red")
        main()
    

if __name__ == "__main__":
    # Afficher la bannière ASCII
    print_banner()

    first_time = get_first_time_running()

    if first_time:
        print(colored("Salut! Il semble que ce soit la première fois que vous exécutez MoneyPrinter V2. Commençons par la configuration!", "yellow"))

    # Configurer l'arborescence des fichiers
    assert_folder_structure()

    # Supprimer les fichiers temporaires
    rem_temp_files()

    # Récupérer les fichiers MP3
    fetch_songs()

    while True:
        main()
