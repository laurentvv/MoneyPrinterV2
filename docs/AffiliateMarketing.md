# Marketing d'affiliation

Cette classe est responsable de la partie Marketing d'Affiliation de MPV2. Elle utilise le package `g4f` (comme toutes les autres classes) pour utiliser la puissance des LLM, dans ce cas, pour générer des tweets, basés sur des informations sur un **Produit Amazon**. MPV2 va scraper la page du produit, et enregistrer le **titre du produit**, et les **caractéristiques du produit**, ayant ainsi assez d'informations pour pouvoir créer un argumentaire pour le produit, et le poster sur Twitter.

## Configuration pertinente

Dans votre `config.json`, vous devez avoir les attributs suivants remplis, pour que le bot puisse fonctionner correctement.

```json
{
  "firefox_profile": "Le chemin vers votre profil Firefox (utilisé pour se connecter à Twitter)",
  "headless": true,
  "llm": "Le Grand Modèle de Langage que vous voulez utiliser pour générer le tweet.",
  "threads": 4
}
```

## Feuille de route

Voici quelques fonctionnalités qui sont prévues pour le futur :

- [ ] Scraper plus d'informations sur le produit, pour pouvoir créer un argumentaire plus détaillé.
- [ ] Rejoindre des communautés en ligne liées au produit, et y poster un argumentaire (avec un lien vers le produit).
- [ ] Répondre aux tweets qui sont liés au produit, avec un argumentaire pour le produit.
