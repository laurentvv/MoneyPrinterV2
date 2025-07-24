# Bot Twitter

Ce bot est conçu pour automatiser le processus de croissance d'un compte Twitter. Une fois que vous avez créé un nouveau compte, fournissez le chemin d'accès au profil Firefox et le bot commencera à publier des tweets en fonction du sujet que vous avez fourni lors de la création du compte.

## Configuration pertinente

Dans votre `config.json`, vous devez remplir les attributs suivants pour que le bot puisse fonctionner correctement.

```json
{
  "twitter_language": "N'importe quelle langue, le formatage n'a pas d'importance",
  "headless": true,
  "llm": "Le grand modèle de langage que vous souhaitez utiliser, consultez Configuration.md pour plus d'informations",
}
```
