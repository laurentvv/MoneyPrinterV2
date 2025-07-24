import os
import json

from typing import List
from config import ROOT_DIR

def get_cache_path() -> str:
    """
    Obtient le chemin vers le fichier de cache.

    Returns:
        path (str): Le chemin vers le dossier de cache
    """
    return os.path.join(ROOT_DIR, '.mp')

def get_afm_cache_path() -> str:
    """
    Obtient le chemin vers le fichier de cache du marketing d'affiliation.

    Returns:
        path (str): Le chemin vers le dossier de cache de l'AFM
    """
    return os.path.join(get_cache_path(), 'afm.json')

def get_twitter_cache_path() -> str:
    """
    Obtient le chemin vers le fichier de cache de Twitter.

    Returns:
        path (str): Le chemin vers le dossier de cache de Twitter
    """
    return os.path.join(get_cache_path(), 'twitter.json')

def get_youtube_cache_path() -> str:
    """
    Obtient le chemin vers le fichier de cache de YouTube.

    Returns:
        path (str): Le chemin vers le dossier de cache de YouTube
    """
    return os.path.join(get_cache_path(), 'youtube.json')

def get_accounts(provider: str) -> List[dict]:
    """
    Obtient les comptes depuis le cache.

    Args:
        provider (str): Le fournisseur pour lequel obtenir les comptes

    Returns:
        account (List[dict]): Les comptes
    """
    cache_path = ""

    if provider == "twitter":
        cache_path = get_twitter_cache_path()
    elif provider == "youtube":
        cache_path = get_youtube_cache_path()

    if not os.path.exists(cache_path):
        # Créer le fichier de cache
        with open(cache_path, 'w') as file:
            json.dump({
                "accounts": []
            }, file, indent=4)

    with open(cache_path, 'r') as file:
        parsed = json.load(file)

        if parsed is None:
            return []
        
        if 'accounts' not in parsed:
            return []

        # Obtenir le dictionnaire des comptes
        return parsed['accounts']

def add_account(provider: str, account: dict) -> None:
    """
    Ajoute un compte au cache.

    Args:
        account (dict): Le compte à ajouter

    Returns:
        None
    """
    if provider == "twitter":
        # Obtenir les comptes actuels
        accounts = get_accounts("twitter")

        # Ajouter le nouveau compte
        accounts.append(account)

        # Écrire les nouveaux comptes dans le cache
        with open(get_twitter_cache_path(), 'w') as file:
            json.dump({
                "accounts": accounts
            }, file, indent=4)
    elif provider == "youtube":
        # Obtenir les comptes actuels
        accounts = get_accounts("youtube")

        # Ajouter le nouveau compte
        accounts.append(account)

        # Écrire les nouveaux comptes dans le cache
        with open(get_youtube_cache_path(), 'w') as file:
            json.dump({
                "accounts": accounts
            }, file, indent=4)

def remove_account(account_id: str) -> None:
    """
    Supprime un compte du cache.

    Args:
        account_id (str): L'ID du compte à supprimer

    Returns:
        None
    """
    # Obtenir les comptes actuels
    accounts = get_accounts()

    # Supprimer le compte
    accounts = [account for account in accounts if account['id'] != account_id]

    # Écrire les nouveaux comptes dans le cache
    with open(get_twitter_cache_path(), 'w') as file:
        json.dump({
            "accounts": accounts
        }, file, indent=4)

def get_products() -> List[dict]:
    """
    Obtient les produits depuis le cache.

    Returns:
        products (List[dict]): Les produits
    """
    if not os.path.exists(get_afm_cache_path()):
        # Créer le fichier de cache
        with open(get_afm_cache_path(), 'w') as file:
            json.dump({
                "products": []
            }, file, indent=4)

    with open(get_afm_cache_path(), 'r') as file:
        parsed = json.load(file)

        # Obtenir les produits
        return parsed["products"]
    
def add_product(product: dict) -> None:
    """
    Ajoute un produit au cache.

    Args:
        product (dict): Le produit à ajouter

    Returns:
        None
    """
    # Obtenir les produits actuels
    products = get_products()

    # Ajouter le nouveau produit
    products.append(product)

    # Écrire les nouveaux produits dans le cache
    with open(get_afm_cache_path(), 'w') as file:
        json.dump({
            "products": products
        }, file, indent=4)
    
def get_results_cache_path() -> str:
    """
    Obtient le chemin vers le fichier de cache des résultats.

    Returns:
        path (str): Le chemin vers le dossier de cache des résultats
    """
    return os.path.join(get_cache_path(), 'scraper_results.csv')
