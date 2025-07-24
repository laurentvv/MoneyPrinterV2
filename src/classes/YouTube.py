import re
import g4f
import json
import time
import requests
import assemblyai as aai

from utils import *
from cache import *
from .Tts import TTS
from config import *
from status import *
from uuid import uuid4
from constants import *
from typing import List
from moviepy.editor import *
from termcolor import colored
from selenium_firefox import *
from selenium import webdriver
from moviepy.video.fx.all import crop
from moviepy.config import change_settings
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from moviepy.video.tools.subtitles import SubtitlesClip
from webdriver_manager.firefox import GeckoDriverManager
from datetime import datetime

# Définir le chemin d'ImageMagick
change_settings({"IMAGEMAGICK_BINARY": get_imagemagick_path()})

class YouTube:
    """
    Classe pour l'automatisation de YouTube.

    Étapes pour créer un YouTube Short:
    1. Générer un sujet [FAIT]
    2. Générer un script [FAIT]
    3. Générer des métadonnées (Titre, Description, Tags) [FAIT]
    4. Générer des prompts d'images IA [FAIT]
    5. Générer des images basées sur les prompts générés [FAIT]
    6. Convertir le texte en parole [FAIT]
    7. Afficher les images chacune pour n secondes, n: Durée du TTS / Nombre d'images [FAIT]
    8. Combiner les images concaténées avec le texte en parole [FAIT]
    """
    def __init__(self, account_uuid: str, account_nickname: str, fp_profile_path: str, niche: str, language: str) -> None:
        """
        Constructeur de la classe YouTube.

        Args:
            account_uuid (str): L'identifiant unique du compte YouTube.
            account_nickname (str): Le surnom du compte YouTube.
            fp_profile_path (str): Chemin vers le profil Firefox connecté au compte YouTube spécifié.
            niche (str): La niche de la chaîne YouTube fournie.
            language (str): La langue de l'automatisation.

        Returns:
            None
        """
        self._account_uuid: str = account_uuid
        self._account_nickname: str = account_nickname
        self._fp_profile_path: str = fp_profile_path
        self._niche: str = niche
        self._language: str = language

        self.images = []

        # Initialiser le profil Firefox
        self.options: Options = Options()
        
        # Définir l'état headless du navigateur
        if get_headless():
            self.options.add_argument("--headless")

        profile = webdriver.FirefoxProfile(self._fp_profile_path)
        self.options.profile = profile

        # Définir le service
        self.service: Service = Service(GeckoDriverManager().install())

        # Initialiser le navigateur
        self.browser: webdriver.Firefox = webdriver.Firefox(service=self.service, options=self.options)

    @property
    def niche(self) -> str:
        """
        Méthode getter pour la niche.

        Returns:
            niche (str): La niche
        """
        return self._niche
    
    @property
    def language(self) -> str:
        """
        Méthode getter pour la langue à utiliser.

        Returns:
            language (str): La langue
        """
        return self._language
    
    def generate_response(self, prompt: str, model: any = None) -> str:
        """
        Génère une réponse LLM basée sur un prompt et le modèle fourni par l'utilisateur.

        Args:
            prompt (str): Le prompt à utiliser dans la génération de texte.

        Returns:
            response (str): La réponse IA générée.
        """
        if not model:
            return g4f.ChatCompletion.create(
                model=parse_model(get_model()),
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
        else:
            return g4f.ChatCompletion.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

    def generate_topic(self) -> str:
        """
        Génère un sujet basé sur la niche de la chaîne YouTube.

        Returns:
            topic (str): Le sujet généré.
        """
        completion = self.generate_response(f"Veuillez générer une idée de vidéo spécifique qui traite du sujet suivant: {self.niche}. Faites-la en une seule phrase exacte. Ne retournez que le sujet, rien d'autre.")

        if not completion:
            error("Échec de la génération du sujet.")

        self.subject = completion

        return completion

    def generate_script(self) -> str:
        """
        Génère un script pour une vidéo, en fonction du sujet de la vidéo, du nombre de paragraphes et du modèle d'IA.

        Returns:
            script (str): Le script de la vidéo.
        """
        sentence_length = get_script_sentence_length()
        prompt = f"""
        Générez un script pour une vidéo de {sentence_length} phrases, en fonction du sujet de la vidéo.

        Le script doit être retourné sous forme de chaîne de caractères avec le nombre de paragraphes spécifié.

        Voici un exemple de chaîne de caractères:
        "Ceci est un exemple de chaîne de caractères."

        Ne faites en aucun cas référence à ce prompt dans votre réponse.

        Allez droit au but, ne commencez pas par des choses inutiles comme, "bienvenue dans cette vidéo".

        Évidemment, le script doit être lié au sujet de la vidéo.
        
        VOUS NE DEVEZ PAS DÉPASSER LA LIMITE DE {sentence_length} PHRASES. ASSUREZ-VOUS QUE LES {sentence_length} PHRASES SONT COURTES.
        VOUS NE DEVEZ INCLURE AUCUN TYPE DE MARKDOWN OU DE FORMATAGE DANS LE SCRIPT, N'UTILISEZ JAMAIS DE TITRE.
        VOUS DEVEZ ÉCRIRE LE SCRIPT DANS LA LANGUE SPÉCIFIÉE DANS [LANGUE].
        RETOURNEZ UNIQUEMENT LE CONTENU BRUT DU SCRIPT. N'INCLUEZ PAS "VOIX OFF", "NARRATEUR" OU DES INDICATEURS SIMILAIRES DE CE QUI DOIT ÊTRE DIT AU DÉBUT DE CHAQUE PARAGRAPHE OU LIGNE. VOUS NE DEVEZ PAS MENTIONNER LE PROMPT, OU QUOI QUE CE SOIT CONCERNANT LE SCRIPT LUI-MÊME. AUSSI, NE PARLEZ JAMAIS DU NOMBRE DE PARAGRAPHES OU DE LIGNES. ÉCRIVEZ SIMPLEMENT LE SCRIPT
        
        Sujet: {self.subject}
        Langue: {self.language}
        """
        completion = self.generate_response(prompt)

        # Appliquer une regex pour supprimer *
        completion = re.sub(r"\*", "", completion)
        
        if not completion:
            error("Le script généré est vide.")
            return
        
        if len(completion) > 5000:
            if get_verbose():
                warning("Le script généré est trop long. Nouvelle tentative...")
            self.generate_script()
        
        self.script = completion
    
        return completion

    def generate_metadata(self) -> dict:
        """
        Génère les métadonnées de la vidéo pour le Short YouTube à téléverser (Titre, Description).

        Returns:
            metadata (dict): Les métadonnées générées.
        """
        title = self.generate_response(f"Veuillez générer un titre de vidéo YouTube pour le sujet suivant, y compris les hashtags: {self.subject}. Ne retournez que le titre, rien d'autre. Limitez le titre à moins de 100 caractères.")

        if len(title) > 100:
            if get_verbose():
                warning("Le titre généré est trop long. Nouvelle tentative...")
            return self.generate_metadata()

        description = self.generate_response(f"Veuillez générer une description de vidéo YouTube pour le script suivant: {self.script}. Ne retournez que la description, rien d'autre.")
        
        self.metadata = {
            "title": title,
            "description": description
        }

        return self.metadata
    
    def generate_prompts(self) -> List[str]:
        """
        Génère des prompts d'images IA basés sur le script vidéo fourni.

        Returns:
            image_prompts (List[str]): Liste générée de prompts d'images.
        """
        # Vérifier si G4F est utilisé pour la génération d'images
        cached_accounts = get_accounts("youtube")
        account_config = None
        for account in cached_accounts:
            if account["id"] == self._account_uuid:
                account_config = account
                break

        # Calculer le nombre de prompts en fonction de la longueur du script
        base_n_prompts = len(self.script) / 3

        # Si G4F est utilisé, limiter à 25 prompts
        if account_config and account_config.get("use_g4f", False):
            n_prompts = min(base_n_prompts, 25)
        else:
            n_prompts = base_n_prompts

        prompt = f"""
        Générez {n_prompts} prompts d'images pour la génération d'images IA,
        en fonction du sujet d'une vidéo.
        Sujet: {self.subject}

        Les prompts d'images doivent être retournés sous forme de
        JSON-Array de chaînes de caractères.

        Chaque terme de recherche doit consister en une phrase complète,
        ajoutez toujours le sujet principal de la vidéo.

        Soyez émotionnel et utilisez des adjectifs intéressants pour rendre le
        prompt d'image aussi détaillé que possible.
        
        VOUS DEVEZ RETOURNER UNIQUEMENT LE JSON-ARRAY DE CHAÎNES DE CARACTÈRES.
        VOUS NE DEVEZ RIEN RETOURNER D'AUTRE.
        VOUS NE DEVEZ PAS RETOURNER LE SCRIPT.
        
        Les termes de recherche doivent être liés au sujet de la vidéo.
        Voici un exemple de JSON-Array de chaînes de caractères:
        ["prompt d'image 1", "prompt d'image 2", "prompt d'image 3"]

        Pour le contexte, voici le texte complet:
        {self.script}
        """

        completion = str(self.generate_response(prompt, model=parse_model(get_image_prompt_llm())))\
            .replace("```json", "") \
            .replace("```", "")

        image_prompts = []

        if "image_prompts" in completion:
            image_prompts = json.loads(completion)["image_prompts"]
        else:
            try:
                image_prompts = json.loads(completion)
                if get_verbose():
                    info(f" => Prompts d'images générés: {image_prompts}")
            except Exception:
                if get_verbose():
                    warning("GPT a retourné une réponse non formatée. Tentative de nettoyage...")

                # Obtenir tout entre [ et ], et le transformer en liste
                r = re.compile(r"\[.*\]")
                image_prompts = r.findall(completion)
                if len(image_prompts) == 0:
                    if get_verbose():
                        warning("Échec de la génération des prompts d'images. Nouvelle tentative...")
                    return self.generate_prompts()

        # Limiter les prompts au nombre maximum autorisé
        if account_config and account_config.get("use_g4f", False):
            image_prompts = image_prompts[:25]
        elif len(image_prompts) > n_prompts:
            image_prompts = image_prompts[:int(n_prompts)]

        self.image_prompts = image_prompts

        success(f"{len(image_prompts)} prompts d'images générés.")

        return image_prompts

    def generate_image_g4f(self, prompt: str) -> str:
        """
        Génère une image IA en utilisant G4F avec SDXL Turbo.

        Args:
            prompt (str): Référence pour la génération d'images

        Returns:
            path (str): Le chemin vers l'image générée.
        """
        print(f"Génération d'une image en utilisant G4F: {prompt}")
        
        try:
            from g4f.client import Client
            
            client = Client()
            response = client.images.generate(
                model="sdxl-turbo",
                prompt=prompt,
                response_format="url"
            )
            
            if response and response.data and len(response.data) > 0:
                # Télécharger l'image depuis l'URL
                image_url = response.data[0].url
                image_response = requests.get(image_url)
                
                if image_response.status_code == 200:
                    image_path = os.path.join(ROOT_DIR, ".mp", str(uuid4()) + ".png")
                    
                    with open(image_path, "wb") as image_file:
                        image_file.write(image_response.content)
                    
                    if get_verbose():
                        info(f" => Image téléchargée depuis {image_url} vers \"{image_path}\"\n")
                    
                    self.images.append(image_path)
                    return image_path
                else:
                    if get_verbose():
                        warning(f"Échec du téléchargement de l'image depuis l'URL: {image_url}")
                    return None
            else:
                if get_verbose():
                    warning("Échec de la génération de l'image en utilisant G4F - pas de données dans la réponse")
                return None
                
        except Exception as e:
            if get_verbose():
                warning(f"Échec de la génération de l'image en utilisant G4F: {str(e)}")
            return None

    def generate_image_cloudflare(self, prompt: str, worker_url: str) -> str:
        """
        Génère une image IA en utilisant un worker Cloudflare.

        Args:
            prompt (str): Référence pour la génération d'images
            worker_url (str): L'URL du worker Cloudflare

        Returns:
            path (str): Le chemin vers l'image générée.
        """
        print(f"Génération d'une image en utilisant Cloudflare: {prompt}")

        url = f"{worker_url}?prompt={prompt}&model=sdxl"
        
        response = requests.get(url)
        
        if response.headers.get('content-type') == 'image/png':
            image_path = os.path.join(ROOT_DIR, ".mp", str(uuid4()) + ".png")
            
            with open(image_path, "wb") as image_file:
                image_file.write(response.content)
            
            if get_verbose():
                info(f" => Image écrite dans \"{image_path}\"\n")
            
            self.images.append(image_path)
            
            return image_path
        else:
            if get_verbose():
                warning("Échec de la génération de l'image. La réponse n'était pas une image PNG.")
            return None

    def generate_image(self, prompt: str) -> str:
        """
        Génère une image IA basée sur le prompt donné.

        Args:
            prompt (str): Référence pour la génération d'images

        Returns:
            path (str): Le chemin vers l'image générée.
        """
        # Obtenir la configuration du compte depuis le cache
        cached_accounts = get_accounts("youtube")
        account_config = None
        for account in cached_accounts:
            if account["id"] == self._account_uuid:
                account_config = account
                break

        if not account_config:
            error("Configuration du compte non trouvée")
            return None

        # Vérifier si G4F ou Cloudflare est utilisé
        if account_config.get("use_g4f", False):
            return self.generate_image_g4f(prompt)
        else:
            worker_url = account_config.get("worker_url")
            if not worker_url:
                error("URL du worker Cloudflare non configurée pour ce compte")
                return None
            return self.generate_image_cloudflare(prompt, worker_url)

    def generate_script_to_speech(self, tts_instance: TTS) -> str:
        """
        Convertit le script généré en parole en utilisant CoquiTTS et retourne le chemin vers le fichier wav.

        Args:
            tts_instance (tts): Instance de la classe TTS.

        Returns:
            path_to_wav (str): Chemin vers l'audio généré (Format WAV).
        """
        path = os.path.join(ROOT_DIR, ".mp", str(uuid4()) + ".wav")

        # Nettoyer le script, supprimer tous les caractères qui ne sont pas un caractère de mot, un espace, un point, un point d'interrogation ou un point d'exclamation.
        self.script = re.sub(r'[^\w\s.?!]', '', self.script)

        tts_instance.synthesize(self.script, path)

        self.tts_path = path

        if get_verbose():
            info(f" => TTS écrit dans \"{path}\"")

        return path
    
    def add_video(self, video: dict) -> None:
        """
        Ajoute une vidéo au cache.

        Args:
            video (dict): La vidéo à ajouter

        Returns:
            None
        """
        videos = self.get_videos()
        videos.append(video)

        cache = get_youtube_cache_path()

        with open(cache, "r") as file:
            previous_json = json.loads(file.read())
            
            # Trouver notre compte
            accounts = previous_json["accounts"]
            for account in accounts:
                if account["id"] == self._account_uuid:
                    account["videos"].append(video)
            
            # Valider les changements
            with open(cache, "w") as f:
                f.write(json.dumps(previous_json))

    def generate_subtitles(self, audio_path: str) -> str:
        """
        Génère des sous-titres pour l'audio en utilisant AssemblyAI.

        Args:
            audio_path (str): Le chemin vers le fichier audio.

        Returns:
            path (str): Le chemin vers le fichier SRT généré.
        """
        # Transformer la vidéo en audio
        aai.settings.api_key = get_assemblyai_api_key()
        config = aai.TranscriptionConfig()
        transcriber = aai.Transcriber(config=config)
        transcript = transcriber.transcribe(audio_path)
        subtitles = transcript.export_subtitles_srt()

        srt_path = os.path.join(ROOT_DIR, ".mp", str(uuid4()) + ".srt")

        with open(srt_path, "w") as file:
            file.write(subtitles)

        return srt_path

    def combine(self) -> str:
        """
        Combine tout dans la vidéo finale.

        Returns:
            path (str): Le chemin vers le fichier MP4 généré.
        """
        combined_image_path = os.path.join(ROOT_DIR, ".mp", str(uuid4()) + ".mp4")
        threads = get_threads()
        tts_clip = AudioFileClip(self.tts_path)
        max_duration = tts_clip.duration
        req_dur = max_duration / len(self.images)

        # Créer un générateur qui retourne un TextClip lorsqu'il est appelé avec des
        generator = lambda txt: TextClip(
            txt,
            font=os.path.join(get_fonts_dir(), get_font()),
            fontsize=100,
            color="#FFFF00",
            stroke_color="black",
            stroke_width=5,
            size=(1080, 1920),
            method="caption",
        )

        print(colored("[+] Combinaison des images...", "blue"))

        clips = []
        tot_dur = 0
        # Ajouter les clips téléchargés encore et encore jusqu'à ce que la durée de l'audio (max_duration) soit atteinte
        while tot_dur < max_duration:
            for image_path in self.images:
                clip = ImageClip(image_path)
                clip.duration = req_dur
                clip = clip.set_fps(30)

                # Toutes les images n'ont pas la même taille,
                # nous devons donc les redimensionner
                if round((clip.w/clip.h), 4) < 0.5625:
                    if get_verbose():
                        info(f" => Redimensionnement de l'image: {image_path} à 1080x1920")
                    clip = crop(clip, width=clip.w, height=round(clip.w/0.5625), \
                                x_center=clip.w / 2, \
                                y_center=clip.h / 2)
                else:
                    if get_verbose():
                        info(f" => Redimensionnement de l'image: {image_path} à 1920x1080")
                    clip = crop(clip, width=round(0.5625*clip.h), height=clip.h, \
                                x_center=clip.w / 2, \
                                y_center=clip.h / 2)
                clip = clip.resize((1080, 1920))

                # FX (Fondu d'entrée)
                #clip = clip.fadein(2)

                clips.append(clip)
                tot_dur += clip.duration

        final_clip = concatenate_videoclips(clips)
        final_clip = final_clip.set_fps(30)
        random_song = choose_random_song()
        
        subtitles_path = self.generate_subtitles(self.tts_path)

        # Égaliser le fichier srt
        equalize_subtitles(subtitles_path, 10)
        
        # Graver les sous-titres dans la vidéo
        subtitles = SubtitlesClip(subtitles_path, generator)

        subtitles.set_pos(("center", "center"))
        random_song_clip = AudioFileClip(random_song).set_fps(44100)

        # Baisser le volume
        random_song_clip = random_song_clip.fx(afx.volumex, 0.1)
        comp_audio = CompositeAudioClip([
            tts_clip.set_fps(44100),
            random_song_clip
        ])

        final_clip = final_clip.set_audio(comp_audio)
        final_clip = final_clip.set_duration(tts_clip.duration)

        # Ajouter les sous-titres
        final_clip = CompositeVideoClip([
            final_clip,
            subtitles
        ])

        final_clip.write_videofile(combined_image_path, threads=threads)

        success(f"Vidéo écrite dans \"{combined_image_path}\"")

        return combined_image_path

    def generate_video(self, tts_instance: TTS) -> str:
        """
        Génère un YouTube Short basé sur la niche et la langue fournies.

        Args:
            tts_instance (TTS): Instance de la classe TTS.

        Returns:
            path (str): Le chemin vers le fichier MP4 généré.
        """
        # Générer le sujet
        self.generate_topic()

        # Générer le script
        self.generate_script()

        # Générer les métadonnées
        self.generate_metadata()

        # Générer les prompts d'images
        self.generate_prompts()

        # Générer les images
        for prompt in self.image_prompts:
            self.generate_image(prompt)

        # Générer le TTS
        self.generate_script_to_speech(tts_instance)

        # Tout combiner
        path = self.combine()

        if get_verbose():
            info(f" => Vidéo générée: {path}")

        self.video_path = os.path.abspath(path)

        return path
    
    def get_channel_id(self) -> str:
        """
        Récupère l'ID de la chaîne du compte YouTube.

        Returns:
            channel_id (str): L'ID de la chaîne.
        """
        driver = self.browser
        driver.get("https://studio.youtube.com")
        time.sleep(2)
        channel_id = driver.current_url.split("/")[-1]
        self.channel_id = channel_id

        return channel_id

    def upload_video(self) -> bool:
        """
        Téléverse la vidéo sur YouTube.

        Returns:
            success (bool): Indique si le téléversement a réussi ou non.
        """
        try:
            self.get_channel_id()

            driver = self.browser
            verbose = get_verbose()

            # Aller sur youtube.com/upload
            driver.get("https://www.youtube.com/upload")

            # Définir le fichier vidéo
            FILE_PICKER_TAG = "ytcp-uploads-file-picker"
            file_picker = driver.find_element(By.TAG_NAME, FILE_PICKER_TAG)
            INPUT_TAG = "input"
            file_input = file_picker.find_element(By.TAG_NAME, INPUT_TAG)
            file_input.send_keys(self.video_path)

            # Attendre la fin du téléversement
            time.sleep(5)

            # Définir le titre
            textboxes = driver.find_elements(By.ID, YOUTUBE_TEXTBOX_ID)

            title_el = textboxes[0]
            description_el = textboxes[-1]

            if verbose:
                info("\t=> Définition du titre...")

            title_el.click()
            time.sleep(1)
            title_el.clear()
            title_el.send_keys(self.metadata["title"])

            if verbose:
                info("\t=> Définition de la description...")

            # Définir la description
            time.sleep(10)
            description_el.click()
            time.sleep(0.5)
            description_el.clear()
            description_el.send_keys(self.metadata["description"])

            time.sleep(0.5)

            # Définir l'option `conçu pour les enfants`
            if verbose:
                info("\t=> Définition de l'option `conçu pour les enfants`...")

            is_for_kids_checkbox = driver.find_element(By.NAME, YOUTUBE_MADE_FOR_KIDS_NAME)
            is_not_for_kids_checkbox = driver.find_element(By.NAME, YOUTUBE_NOT_MADE_FOR_KIDS_NAME)

            if not get_is_for_kids():
                is_not_for_kids_checkbox.click()
            else:
                is_for_kids_checkbox.click()

            time.sleep(0.5)

            # Cliquer sur suivant
            if verbose:
                info("\t=> Clic sur suivant...")

            next_button = driver.find_element(By.ID, YOUTUBE_NEXT_BUTTON_ID)
            next_button.click()

            # Cliquer à nouveau sur suivant
            if verbose:
                info("\t=> Clic à nouveau sur suivant...")
            next_button = driver.find_element(By.ID, YOUTUBE_NEXT_BUTTON_ID)
            next_button.click()

            # Attendre 2 secondes
            time.sleep(2)

            # Cliquer à nouveau sur suivant
            if verbose:
                info("\t=> Clic à nouveau sur suivant...")
            next_button = driver.find_element(By.ID, YOUTUBE_NEXT_BUTTON_ID)
            next_button.click()

            # Définir comme non répertorié
            if verbose:
                info("\t=> Définition comme non répertorié...")
            
            radio_button = driver.find_elements(By.XPATH, YOUTUBE_RADIO_BUTTON_XPATH)
            radio_button[2].click()

            if verbose:
                info("\t=> Clic sur le bouton terminé...")

            # Cliquer sur le bouton terminé
            done_button = driver.find_element(By.ID, YOUTUBE_DONE_BUTTON_ID)
            done_button.click()

            # Attendre 2 secondes
            time.sleep(2)

            # Obtenir la dernière vidéo
            if verbose:
                info("\t=> Obtention de l'URL de la vidéo...")

            # Obtenir l'URL de la dernière vidéo téléversée
            driver.get(f"https://studio.youtube.com/channel/{self.channel_id}/videos/short")
            time.sleep(2)
            videos = driver.find_elements(By.TAG_NAME, "ytcp-video-row")
            first_video = videos[0]
            anchor_tag = first_video.find_element(By.TAG_NAME, "a")
            href = anchor_tag.get_attribute("href")
            if verbose:
                info(f"\t=> Extraction de l'ID de la vidéo depuis l'URL: {href}")
            video_id = href.split("/")[-2]

            # Construire l'URL
            url = build_url(video_id)

            self.uploaded_video_url = url

            if verbose:
                success(f" => Vidéo téléversée: {url}")

            # Ajouter la vidéo au cache
            self.add_video({
                "title": self.metadata["title"],
                "description": self.metadata["description"],
                "url": url,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            # Fermer le navigateur
            driver.quit()

            return True
        except:
            self.browser.quit()
            return False


    def get_videos(self) -> List[dict]:
        """
        Récupère les vidéos téléversées de la chaîne YouTube.

        Returns:
            videos (List[dict]): Les vidéos téléversées.
        """
        if not os.path.exists(get_youtube_cache_path()):
            # Créer le fichier de cache
            with open(get_youtube_cache_path(), 'w') as file:
                json.dump({
                    "videos": []
                }, file, indent=4)
            return []

        videos = []
        # Lire le fichier de cache
        with open(get_youtube_cache_path(), 'r') as file:
            previous_json = json.loads(file.read())
            # Trouver notre compte
            accounts = previous_json["accounts"]
            for account in accounts:
                if account["id"] == self._account_uuid:
                    videos = account["videos"]

        return videos
