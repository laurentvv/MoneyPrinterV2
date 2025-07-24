import os
import sys
import site

from config import ROOT_DIR
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer

class TTS:
    """
    Classe pour la synthèse vocale utilisant Coqui TTS.
    """
    def __init__(self) -> None:
        """
        Initialise la classe TTS.

        Returns:
            None
        """
        # Détecter les paquets de site de l'environnement virtuel
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            # Nous sommes dans un environnement virtuel
            site_packages = site.getsitepackages()[0]
        else:
            # Nous ne sommes pas dans un environnement virtuel, utilisez les paquets de site de l'utilisateur
            site_packages = site.getusersitepackages()

        # Chemin vers le fichier .models.json
        models_json_path = os.path.join(
            site_packages,
            "TTS",
            ".models.json",
        )

        # Créer le répertoire s'il n'existe pas
        tts_dir = os.path.dirname(models_json_path)
        if not os.path.exists(tts_dir):
            os.makedirs(tts_dir)

        # Initialiser le ModelManager
        self._model_manager = ModelManager(models_json_path)

        # Télécharger tts_models/en/ljspeech/fast_pitch
        self._model_path, self._config_path, self._model_item = \
            self._model_manager.download_model("tts_models/en/ljspeech/tacotron2-DDC_ph")

        # Télécharger vocoder_models/en/ljspeech/hifigan_v2 comme notre vocodeur
        voc_path, voc_config_path, _ = self._model_manager. \
            download_model("vocoder_models/en/ljspeech/univnet")
        
        # Initialiser le Synthesizer
        self._synthesizer = Synthesizer(
            tts_checkpoint=self._model_path,
            tts_config_path=self._config_path,
            vocoder_checkpoint=voc_path,
            vocoder_config=voc_config_path
        )

    @property
    def synthesizer(self) -> Synthesizer:
        """
        Retourne le synthétiseur.

        Returns:
            Synthesizer: Le synthétiseur.
        """
        return self._synthesizer

    def synthesize(self, text: str, output_file: str = os.path.join(ROOT_DIR, ".mp", "audio.wav")) -> str:
        """
        Synthétise le texte donné en parole.

        Args:
            text (str): Le texte à synthétiser.
            output_file (str, optional): Le fichier de sortie pour enregistrer la parole synthétisée. Par défaut, "audio.wav".

        Returns:
            str: Le chemin vers le fichier de sortie.
        """
        # Synthétiser le texte
        outputs = self.synthesizer.tts(text)

        # Enregistrer la parole synthétisée dans le fichier de sortie
        self.synthesizer.save_wav(outputs, output_file)

        return output_file
