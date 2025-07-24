# Configuration

Toutes vos configurations se trouveront dans un fichier dans le répertoire racine, appelé `config.json`, qui est une copie de `config.example.json`. Vous pouvez modifier les valeurs dans `config.json` à votre guise.

## Valeurs

- `verbose`: `boolean` - Si `true`, l'application affichera plus d'informations.
- `firefox_profile`: `string` - Le chemin vers votre profil Firefox. Ceci est utilisé pour utiliser vos comptes de médias sociaux sans avoir à vous connecter à chaque fois que vous exécutez l'application.
- `headless`: `boolean` - Si `true`, l'application s'exécutera en mode headless. Cela signifie que le navigateur ne sera pas visible.
- `llm`: Ceci décidera du Grand Modèle de Langage que MPV2 utilise pour générer des tweets, des scripts, des invites d'image et plus encore. Si laissé vide, le modèle par défaut (`gpt35_turbo`) sera utilisé. Voici vos choix :
    * `gpt4`
    * `gpt35_turbo`
    * `llama2_7b`
    * `llama2_13b`
    * `llama2_70b`
    * `mixtral_8x7b`
- `image_prompt_llm`: `string` - Le Grand Modèle de Langage qui sera utilisé pour générer des invites d'image. Si laissé vide, le modèle par défaut (`gpt35_turbo`) sera utilisé. Voici vos choix :
    * `gpt4`
    * `gpt35_turbo`
    * `llama2_7b`
    * `llama2_13b`
    * `llama2_70b`
    * `mixtral_8x7b`
- `twitter_language`: `string` - La langue qui sera utilisée pour générer et poster des tweets.
- `image_model`: `string` - Quel modèle d'IA vous voulez utiliser pour générer des images, voici vos choix :
    * `v1`
    * `v2`
    * `v3` (DALL-E)
    * `lexica`
    * `prodia`
    * `simurg`
    * `animefy`
    * `raava`
    * `shonin`
- `threads`: `number` - Le nombre de threads qui seront utilisés pour exécuter des opérations, par exemple, écrire dans un fichier en utilisant MoviePy.
- `is_for_kids`: `boolean` - Si `true`, l'application téléchargera la vidéo sur YouTube Shorts comme une vidéo pour les enfants.
- `google_maps_scraper`: `string` - L'URL du scraper de Google Maps. Ceci sera utilisé pour scraper Google Maps pour les entreprises locales. Il est recommandé d'utiliser la valeur par défaut.
- `zip_url`: `string` - L'URL du fichier ZIP qui contient les chansons à utiliser pour l'Automateur de YouTube Shorts.
- `email`: `object`:
    - `smtp_server`: `string` - Votre serveur SMTP.
    - `smtp_port`: `number` - Le port de votre serveur SMTP.
    - `username`: `string` - Votre adresse e-mail.
    - `password`: `string` - Votre mot de passe e-mail.
- `google_maps_scraper_niche`: `string` - La niche que vous voulez scraper sur Google Maps.
- `scraper_timeout`: `number` - Le timeout pour le scraper de Google Maps.
- `outreach_message_subject`: `string` - Le sujet de votre message de prospection. `{{COMPANY_NAME}}` sera remplacé par le nom de l'entreprise.
- `outreach_message_body_file`: `string` - Le fichier qui contient le corps de votre message de prospection, devrait être en HTML. `{{COMPANY_NAME}}` sera remplacé par le nom de l'entreprise.
- `assembly_ai_api_key`: `string` - Votre clé API Assembly AI. Obtenez la vôtre [ici](https://www.assemblyai.com/app/).
- `font`: `string` - La police qui sera utilisée pour générer des images. Ce devrait être un fichier `.ttf` dans le répertoire `fonts/`.
- `imagemagick_path`: `string` - Le chemin vers le binaire ImageMagick. Ceci est utilisé par MoviePy pour manipuler des images. Installez ImageMagick depuis [ici](https://imagemagick.org/script/download.php) et définissez le chemin vers le `magick.exe` sous Windows, ou sous Linux/MacOS le chemin vers `convert` (généralement /usr/bin/convert).

## Exemple

```json
{
  "verbose": true,
  "firefox_profile": "",
  "headless": false,
  "twitter_language": "English",
  "llm": "gpt4",
  "image_prompt_llm": "gpt35_turbo",
  "image_model": "prodia",
  "threads": 2,
  "zip_url": "",
  "is_for_kids": false,
  "google_maps_scraper": "https://github.com/gosom/google-maps-scraper/archive/refs/tags/v0.9.7.zip",
  "email": {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "username": "",
    "password": ""
  },
  "google_maps_scraper_niche": "",
  "scraper_timeout": 300,
  "outreach_message_subject": "I have a question...",
  "outreach_message_body_file": "outreach_message.html",
  "assembly_ai_api_key": "",
  "font": "bold_font.ttf",
  "imagemagick_path": "C:\\Program Files\\ImageMagick-7.1.0-Q16\\magick.exe"
}
```
