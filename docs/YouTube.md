# Automateur de YouTube Shorts

MPV2 utilise une implémentation similaire à celle de V1 (voir [MPV1](https://github.com/FujiwaraChoki/MoneyPrinter)), pour générer des fichiers vidéo et les télécharger sur YouTube Shorts.

Contrairement à V1, V2 utilise des images générées par IA comme visuels pour la vidéo, au lieu d'utiliser des séquences d'archives. Cela rend les vidéos plus uniques et moins susceptibles d'être signalées par YouTube. V2 prend également en charge la musique dès le départ.

## Configuration pertinente

Dans votre `config.json`, vous devez remplir les attributs suivants pour que le bot puisse fonctionner correctement.

```json
{
  "firefox_profile": "Le chemin d'accès à votre profil Firefox (utilisé pour vous connecter à YouTube)",
  "headless": true,
  "llm": "Le grand modèle de langage que vous souhaitez utiliser pour générer le script de la vidéo.",
  "image_model": "Le modèle d'IA que vous souhaitez utiliser pour générer des images.",
  "threads": 4,
  "is_for_kids": true
}
```

## Feuille de route

Voici quelques fonctionnalités prévues pour l'avenir :

- [ ] Sous-titres (en utilisant AssemblyAI ou en les assemblant localement)
