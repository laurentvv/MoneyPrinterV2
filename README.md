# MoneyPrinterV2

[![madewithlove](https://img.shields.io/badge/made_with-%E2%9D%A4-red?style=for-the-badge&labelColor=orange)](https://github.com/FujiwaraChoki/MoneyPrinterV2)
[![Offrez-moi un café](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Donate-brightgreen?logo=buymeacoffee)](https://www.buymeacoffee.com/fujicodes)
[![Licence GitHub](https://img.shields.io/github/license/FujiwaraChoki/MoneyPrinterV2?style=for-the-badge)](https://github.com/FujiwaraChoki/MoneyPrinterV2/blob/main/LICENSE)
[![Problèmes GitHub](https://img.shields.io/github/issues/FujiwaraChoki/MoneyPrinterV2?style=for-the-badge)](https://github.com/FujiwaraChoki/MoneyPrinterV2/issues)
[![Étoiles GitHub](https://img.shields.io/github/stars/FujiwaraChoki/MoneyPrinterV2?style=for-the-badge)](https://github.com/FujiwaraChoki/MoneyPrinterV2/stargazers)
[![Discord](https://img.shields.io/discord/1134848537704804432?style=for-the-badge)](https://dsc.gg/fuji-community)

> **Sponsor**: La meilleure application de chat IA : [shiori.ai](https://www.shiori.ai)
> **Suivez-moi sur X**: [@DevBySami](https://x.com/DevBySami)

## À propos du projet

MoneyPrinterV2 (MPV2) est une application puissante et polyvalente conçue pour automatiser diverses méthodes de monétisation en ligne. C'est une réécriture complète de la version originale, avec une architecture modulaire et un ensemble de fonctionnalités étendues.

> **Note importante**: MPV2 nécessite Python 3.9 pour fonctionner correctement.

## Fonctionnalités

MPV2 offre une suite d'outils pour vous aider à automatiser vos activités en ligne :

- **🤖 Bot Twitter**: Automatisez vos publications, interagissez avec d'autres utilisateurs et gérez votre compte Twitter de manière efficace.
- **🎬 Automatisation de YouTube Shorts**: Créez et publiez des YouTube Shorts de manière automatisée pour développer votre audience.
- **📈 Marketing d'affiliation**: Intégrez des liens d'affiliation Amazon dans vos publications Twitter pour monétiser votre contenu.
- ** outreach**: Trouvez des entreprises locales et contactez-les de manière automatisée pour proposer vos services.

## Installation

Pour commencer à utiliser MPV2, suivez ces étapes :

### Prérequis

1.  **Python 3.9**: Assurez-vous d'avoir Python 3.9 installé sur votre système.
2.  **Microsoft Visual C++ Build Tools**: Installez les [outils de build Microsoft Visual C++](https://visualstudio.microsoft.com/de/visual-cpp-build-tools/) pour que CoquiTTS fonctionne correctement.
3.  **Langage de programmation Go**: Si vous prévoyez d'utiliser la fonctionnalité d'envoi d'e-mails, installez [Go](https://golang.org/).

### Étapes d'installation

1.  **Clonez le dépôt**:
    ```bash
    git clone https://github.com/FujiwaraChoki/MoneyPrinterV2.git
    ```
2.  **Accédez au répertoire du projet**:
    ```bash
    cd MoneyPrinterV2
    ```
3.  **Configurez l'application**:
    -   Copiez le fichier de configuration d'exemple :
        ```bash
        cp config.example.json config.json
        ```
    -   Ouvrez `config.json` et remplissez les valeurs requises.
4.  **Créez et activez un environnement virtuel**:
    -   Créez l'environnement :
        ```bash
        python -m venv venv
        ```
    -   Activez-le :
        -   **Windows**: `.\venv\Scripts\activate`
        -   **Unix/macOS**: `source venv/bin/activate`
5.  **Installez les dépendances**:
    ```bash
    pip install -r requirements.txt
    ```

## Utilisation

Une fois l'installation terminée, vous pouvez lancer l'application avec la commande suivante :

```bash
python src/main.py
```

## Documentation

Pour plus de détails sur la configuration et l'utilisation avancée, consultez notre [documentation](docs/).

## Scripts

Le répertoire `scripts` contient des scripts utiles pour accéder directement aux fonctionnalités principales de MPV2 sans interaction manuelle.

Exécutez-les depuis la racine du projet :

```bash
bash scripts/upload_video.sh
```

## Foire aux questions (FAQ)

**Q : Comment puis-je obtenir de l'aide ?**

**R :** Le meilleur moyen d'obtenir de l'aide est de rejoindre notre [serveur Discord](https://dsc.gg/fuji-community).

**Q : Comment puis-je contribuer au projet ?**

**R :** Nous apprécions les contributions de la communauté. Veuillez lire notre [guide de contribution](CONTRIBUTING.md) et consulter notre [feuille de route](docs/Roadmap.md) pour voir les fonctionnalités que nous prévoyons d'ajouter.

**Q : Le projet est-il gratuit ?**

**R :** Oui, MoneyPrinterV2 est un projet open source sous licence `Affero General Public License v3.0`.

## Contribuer

Les contributions sont les bienvenues ! Veuillez lire le fichier [CONTRIBUTING.md](CONTRIBUTING.md) pour savoir comment participer.

## Licence

Ce projet est sous licence `Affero General Public License v3.0`. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Avertissement

Ce projet est à des fins éducatives uniquement. L'auteur ne sera pas responsable de toute utilisation abusive des informations fournies. Utilisez ce projet à vos propres risques.
