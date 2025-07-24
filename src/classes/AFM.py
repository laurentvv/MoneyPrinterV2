import g4f

from status import *
from config import *
from constants import *
from .Twitter import Twitter
from selenium_firefox import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

class AffiliateMarketing:
    """
    Cette classe sera utilisée pour gérer toutes les opérations liées au marketing d'affiliation.
    """
    def __init__(self, affiliate_link: str, fp_profile_path: str, twitter_account_uuid: str, account_nickname: str, topic: str) -> None:
        """
        Initialise la classe Affiliate Marketing.

        Args:
            affiliate_link (str): Le lien d'affiliation
            fp_profile_path (str): Le chemin vers le profil Firefox
            twitter_account_uuid (str): L'UUID du compte Twitter
            account_nickname (str): Le surnom du compte
            topic (str): Le sujet du produit

        Returns:
            None
        """
        self._fp_profile_path: str = fp_profile_path

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

        # Définir le lien d'affiliation
        self.affiliate_link: str = affiliate_link

        # Définir l'UUID du compte Twitter
        self.account_uuid: str = twitter_account_uuid

        # Définir le surnom du compte Twitter
        self.account_nickname: str = account_nickname

        # Définir le sujet Twitter
        self.topic: str = topic

        # Scraper les informations sur le produit
        self.scrape_product_information()

    def scrape_product_information(self) -> None:
        """
        Cette méthode sera utilisée pour scraper les informations sur le produit
        à partir du lien d'affiliation.
        """
        # Ouvrir le lien d'affiliation
        self.browser.get(self.affiliate_link)

        # Obtenir le nom du produit
        product_title: str = self.browser.find_element(By.ID, AMAZON_PRODUCT_TITLE_ID).text
        
        # Obtenir les caractéristiques du produit
        features: any = self.browser.find_elements(By.ID, AMAZON_FEATURE_BULLETS_ID)

        if get_verbose():
            info(f"Titre du produit: {product_title}")

        if get_verbose():
            info(f"Caractéristiques: {features}")
            
        # Définir le titre du produit
        self.product_title: str = product_title

        # Définir les caractéristiques
        self.features: any = features

    def generate_response(self, prompt: str) -> str:
        """
        Cette méthode sera utilisée pour générer la réponse pour l'utilisateur.

        Args:
            prompt (str): Le prompt pour l'utilisateur.

        Returns:
            response (str): La réponse pour l'utilisateur.
        """
        # Générer la réponse
        response: str = g4f.ChatCompletion.create(
            model=parse_model(get_model()),
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Retourner la réponse
        return response

    def generate_pitch(self) -> str:
        """
        Cette méthode sera utilisée pour générer un argumentaire pour le produit.

        Returns:
            pitch (str): L'argumentaire pour le produit.
        """
        # Générer la réponse
        pitch: str = self.generate_response(f"Je veux promouvoir ce produit sur mon site web. Générez un bref argumentaire sur ce produit, ne retournez rien d'autre que l'argumentaire. Informations:\nTitre: \"{self.product_title}\"\nCaractéristiques: \"{str(self.features)}\"") + "\nVous pouvez acheter le produit ici: " + self.affiliate_link

        self.pitch: str = pitch

        # Retourner la réponse
        return pitch
    
    def share_pitch(self, where: str) -> None:
        """
        Cette méthode sera utilisée pour partager l'argumentaire sur la plateforme spécifiée.

        Args:
            where (str): La plateforme où l'argumentaire sera partagé.
        """
        if where == "twitter":
            # Initialiser la classe Twitter
            twitter: Twitter = Twitter(self.account_uuid, self.account_nickname, self._fp_profile_path, self.topic)

            # Partager l'argumentaire
            twitter.post(self.pitch)

    def quit(self) -> None:
        """
        Cette méthode sera utilisée pour quitter le navigateur.
        """
        # Quitter le navigateur
        self.browser.quit()
