import re
import g4f
import sys
import time

from cache import *
from config import *
from status import *
from constants import *
from typing import List
from datetime import datetime
from termcolor import colored
from selenium_firefox import *
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager


class Twitter:
    """
    Classe pour le Bot, qui fait grandir un compte Twitter.
    """
    def __init__(self, account_uuid: str, account_nickname: str, fp_profile_path: str, topic: str) -> None:
        """
        Initialise le Bot Twitter.

        Args:
            account_uuid (str): L'UUID du compte
            account_nickname (str): Le surnom du compte
            fp_profile_path (str): Le chemin vers le profil Firefox

        Returns:
            None
        """
        self.account_uuid: str = account_uuid
        self.account_nickname: str = account_nickname
        self.fp_profile_path: str = fp_profile_path
        self.topic: str = topic

        # Initialiser le profil Firefox
        self.options: Options = Options()
        
        # Définir l'état headless du navigateur
        if get_headless():
            self.options.add_argument("--headless")

        # Définir le chemin du profil
        self.options.add_argument("-profile")
        self.options.add_argument(fp_profile_path)

        # Définir le service
        self.service: Service = Service(GeckoDriverManager().install())

        # Initialiser le navigateur
        self.browser: webdriver.Firefox = webdriver.Firefox(service=self.service, options=self.options)

    def post(self, text: str = None) -> None:
        """
        Démarre le Bot Twitter.

        Args:
            text (str): Le texte à publier

        Returns:
            None
        """
        bot: webdriver.Firefox = self.browser
        verbose: bool = get_verbose()

        bot.get("https://twitter.com")

        time.sleep(2)

        post_content: str = self.generate_post()
        now: datetime = datetime.now()

        print(colored(f" => Publication sur Twitter:", "blue"), post_content[:30] + "...")

        try:
            bot.find_element(By.XPATH, "//a[@data-testid='SideNav_NewTweet_Button']").click()
        except exceptions.NoSuchElementException:
            time.sleep(3)
            bot.find_element(By.XPATH, "//a[@data-testid='SideNav_NewTweet_Button']").click()

        time.sleep(2) 
        body = post_content if text is None else text

        try:
            bot.find_element(By.XPATH, "//div[@role='textbox']").send_keys(body)
        except exceptions.NoSuchElementException:
            time.sleep(2)
            bot.find_element(By.XPATH, "//div[@role='textbox']").send_keys(body)

        time.sleep(1)
        bot.find_element(By.CLASS_NAME, "notranslate").send_keys(keys.Keys.ENTER)
        bot.find_element(By.XPATH, "//button[@data-testid='tweetButton']").click()

        if verbose:
            print(colored(" => Bouton [ENTRÉE] pressé sur Twitter..", "blue"))
        time.sleep(4)

        # Ajouter la publication au cache
        self.add_post({
            "content": post_content,
            "date": now.strftime("%m/%d/%Y, %H:%M:%S")
        })

        success("Publié sur Twitter avec succès!")


    def get_posts(self) -> List[dict]:
        """
        Récupère les publications du cache.

        Returns:
            posts (List[dict]): Les publications
        """
        if not os.path.exists(get_twitter_cache_path()):
            # Créer le fichier de cache
            with open(get_twitter_cache_path(), 'w') as file:
                json.dump({
                    "posts": []
                }, file, indent=4)

        with open(get_twitter_cache_path(), 'r') as file:
            parsed = json.load(file)

            # Trouver notre compte
            accounts = parsed["accounts"]
            for account in accounts:
                if account["id"] == self.account_uuid:
                    posts = account["posts"]

                    if posts is None:
                        return []

                    # Retourner les publications
                    return posts
        
    def add_post(self, post: dict) -> None:
        """
        Ajoute une publication au cache.

        Args:
            post (dict): La publication à ajouter

        Returns:
            None
        """
        posts = self.get_posts()
        posts.append(post)

        with open(get_twitter_cache_path(), "r") as file:
            previous_json = json.loads(file.read())
            
            # Trouver notre compte
            accounts = previous_json["accounts"]
            for account in accounts:
                if account["id"] == self.account_uuid:
                    account["posts"].append(post)
            
            # Valider les changements
            with open(get_twitter_cache_path(), "w") as f:
                f.write(json.dumps(previous_json))
            

    def generate_post(self) -> str:
        """
        Génère une publication pour le compte Twitter en fonction du sujet.

        Returns:
            post (str): La publication
        """
        completion = g4f.ChatCompletion.create(
            model=parse_model(get_model()),
            messages=[
                {
                    "role": "user",
                    "content": f"Générez une publication Twitter sur: {self.topic} en {get_twitter_language()}. La limite est de 2 phrases. Choisissez un sous-sujet spécifique du sujet fourni."
                }
            ]
        )

        if get_verbose():
            info("Génération d'une publication...")

        if completion is None:
            error("Échec de la génération d'une publication. Veuillez réessayer.")
            sys.exit(1)

        # Appliquer Regex pour supprimer tous les *
        completion = re.sub(r"\*", "", completion).replace("\"", "")
    
        if get_verbose():
            info(f"Longueur de la publication: {len(completion)}")
        if len(completion) >= 260:
            return self.generate_post()

        return completion
