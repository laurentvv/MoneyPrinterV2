import os
import io
import re
import csv
import time
import zipfile
import yagmail
import requests
import subprocess

from cache import *
from status import *
from config import *

class Outreach:
    """
    Classe qui héberge les méthodes pour contacter les entreprises.
    """
    def __init__(self) -> None:
        """
        Constructeur de la classe Outreach.

        Returns:
            None
        """
        # Vérifier si go est installé
        self.go_installed = os.system("go version") == 0

        # Définir la niche
        self.niche = get_google_maps_scraper_niche()

        # Définir les informations d'identification de l'e-mail
        self.email_creds = get_email_credentials()

    def is_go_installed(self) -> bool:
        """
        Vérifie si go est installé.

        Returns:
            bool: True si go est installé, False sinon.
        """
        # Vérifier si go est installé
        try:
            subprocess.call("go version", shell=True)
            return True
        except Exception as e:
            return False

    def unzip_file(self, zip_link: str) -> None:
        """
        Décompresse le fichier.

        Args:
            zip_link (str): Le lien vers le fichier zip.

        Returns:
            None
        """
        # Vérifier si le scraper est déjà décompressé, sinon, le décompresser
        if os.path.exists("google-maps-scraper-0.9.7"):
            info("=> Scraper déjà décompressé. Saut de la décompression.")
            return

        r = requests.get(zip_link)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall()

    def build_scraper(self) -> None:
        """
        Construit le scraper.

        Returns:
            None
        """
        # Vérifier si le scraper est déjà construit, sinon, le construire
        if os.path.exists("google-maps-scraper.exe"):
            print(colored("=> Scraper déjà construit. Saut de la construction.", "blue"))
            return

        os.chdir("google-maps-scraper-0.9.7")
        os.system("go mod download")
        os.system("go build")
        os.system("mv google-maps-scraper ../google-maps-scraper")
        os.chdir("..")

    def run_scraper_with_args_for_30_seconds(self, args: str, timeout = 300) -> None:
        """
        Exécute le scraper avec les arguments spécifiés pendant 30 secondes.

        Args:
            args (str): Les arguments avec lesquels exécuter le scraper.
            timeout (int): Le temps d'exécution du scraper.

        Returns:
            None
        """
        # Exécuter le scraper avec les arguments spécifiés
        info(" => Exécution du scraper...")
        command = "google-maps-scraper " + args
        try:
            scraper_process = subprocess.call(command.split(" "), shell=True, timeout=float(timeout))

            if scraper_process == 0:
                subprocess.call("taskkill /f /im google-maps-scraper.exe", shell=True)
                print(colored("=> Le scraper s'est terminé avec succès.", "green"))
            else:
                subprocess.call("taskkill /f /im google-maps-scraper.exe", shell=True)
                print(colored("=> Le scraper s'est terminé avec une erreur.", "red"))
            
        except Exception as e:
            subprocess.call("taskkill /f /im google-maps-scraper.exe", shell=True)
            print(colored("Une erreur s'est produite lors de l'exécution du scraper:", "red"))
            print(str(e))

    def get_items_from_file(self, file_name: str) -> list:
        """
        Lit et retourne les éléments d'un fichier.

        Args:
            file_name (str): Le nom du fichier à lire.

        Returns:
            list: Les éléments du fichier.
        """
        # Lire et retourner les éléments d'un fichier
        with open(file_name, "r", errors="ignore") as f:
            items = f.readlines()
            items = [item.strip() for item in items[1:]]
            return items
        
    def set_email_for_website(self, index: int, website: str, output_file: str):
        """Extrait une adresse e-mail d'un site web et met à jour un fichier CSV avec celle-ci.

        Cette méthode envoie une requête GET au site web spécifié, recherche la
        première adresse e-mail dans le contenu HTML et l'ajoute à la ligne spécifiée
        dans un fichier CSV. Si aucune adresse e-mail n'est trouvée, aucune modification n'est apportée au
        fichier CSV.

        Args:
            index (int): L'index de la ligne dans le fichier CSV où l'e-mail doit être ajouté.
            website (str): L'URL du site web d'où extraire l'adresse e-mail.
            output_file (str): Le chemin vers le fichier CSV à mettre à jour avec l'e-mail extrait.
        """
        # Extraire et définir un e-mail pour un site web
        email = ""

        r = requests.get(website)
        if r.status_code == 200:
            # Définir une expression régulière pour correspondre aux adresses e-mail
            email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"

            # Trouver toutes les adresses e-mail dans la chaîne HTML
            email_addresses = re.findall(email_pattern, r.text)

            email = email_addresses[0] if len(email_addresses) > 0 else ""

        if email:
            print(f"=> Définition de l'e-mail {email} pour le site web {website}")
            with open(output_file, "r", newline="", errors="ignore") as csvfile:
                csvreader = csv.reader(csvfile)
                items = list(csvreader)
                items[index].append(email)

            with open(output_file, "w", newline="", errors="ignore") as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerows(items)
        
    def start(self) -> None:
        """
        Démarre le processus de prospection.

        Returns:
            None
        """
        # Vérifier si go est installé
        if not self.is_go_installed():
            error("Go n'est pas installé. Veuillez installer go et réessayer.")
            return

        # Décompresser le scraper
        self.unzip_file(get_google_maps_scraper_zip_url())

        # Construire le scraper
        self.build_scraper()

        # Écrire la niche dans un fichier
        with open("niche.txt", "w") as f:
            f.write(self.niche)

        output_path = get_results_cache_path()
        message_subject = get_outreach_message_subject()
        message_body = get_outreach_message_body_file()

        # Exécuter
        self.run_scraper_with_args_for_30_seconds(f"-input niche.txt -results \"{output_path}\"", timeout=get_scraper_timeout())

        # Obtenir les éléments du fichier
        items = self.get_items_from_file(output_path)
        success(f" => {len(items)} éléments scrapés.")

        # Supprimer le fichier de niche
        os.remove("niche.txt")

        time.sleep(2)

        # Créer un client SMTP yagmail en dehors de la boucle
        yag = yagmail.SMTP(user=self.email_creds["username"], password=self.email_creds["password"], host=self.email_creds["smtp_server"], port=self.email_creds["smtp_port"])

        # Obtenir l'e-mail pour chaque entreprise
        for item in items:
            try:
                # Vérifier si le site web de l'élément est valide
                website = item.split(",")
                website = [w for w in website if w.startswith("http")]
                website = website[0] if len(website) > 0 else ""
                if website != "":
                    test_r = requests.get(website)
                    if test_r.status_code == 200:
                        self.set_email_for_website(items.index(item), website, output_path)
                        
                        # Envoyer des e-mails en utilisant la connexion SMTP existante
                        receiver_email = item.split(",")[-1]

                        if "@" not in receiver_email:
                            warning(f" => Aucun e-mail fourni. Saut...")
                            continue

                        subject = message_subject.replace("{{COMPANY_NAME}}", item[0])
                        body = open(message_body, "r").read().replace("{{COMPANY_NAME}}", item[0])

                        info(f" => Envoi de l'e-mail à {receiver_email}...")
                        
                        yag.send(
                            to=receiver_email,
                            subject=subject,
                            contents=body,
                        )

                        success(f" => E-mail envoyé à {receiver_email}")
                    else:
                        warning(f" => Le site web {website} est invalide. Saut...")
            except Exception as err:
                error(f" => Erreur: {err}...")
                continue
