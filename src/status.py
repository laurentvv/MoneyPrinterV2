from termcolor import colored

def error(message: str, show_emoji: bool = True) -> None:
    """
    Affiche un message d'erreur.

    Args:
        message (str): Le message d'erreur
        show_emoji (bool): Indique si l'emoji doit être affiché

    Returns:
        None
    """
    emoji = "❌" if show_emoji else ""
    print(colored(f"{emoji} {message}", "red"))

def success(message: str, show_emoji: bool = True) -> None:
    """
    Affiche un message de succès.

    Args:
        message (str): Le message de succès
        show_emoji (bool): Indique si l'emoji doit être affiché

    Returns:
        None
    """
    emoji = "✅" if show_emoji else ""
    print(colored(f"{emoji} {message}", "green"))

def info(message: str, show_emoji: bool = True) -> None:
    """
    Affiche un message d'information.

    Args:
        message (str): Le message d'information
        show_emoji (bool): Indique si l'emoji doit être affiché

    Returns:
        None
    """
    emoji = "ℹ️" if show_emoji else ""
    print(colored(f"{emoji} {message}", "magenta"))

def warning(message: str, show_emoji: bool = True) -> None:
    """
    Affiche un message d'avertissement.

    Args:
        message (str): Le message d'avertissement
        show_emoji (bool): Indique si l'emoji doit être affiché

    Returns:
        None
    """
    emoji = "⚠️" if show_emoji else ""
    print(colored(f"{emoji} {message}", "yellow"))

def question(message: str, show_emoji: bool = True) -> str:
    """
    Affiche une question et retourne la saisie de l'utilisateur.

    Args:
        message (str): Le message de la question
        show_emoji (bool): Indique si l'emoji doit être affiché

    Returns:
        user_input (str): La saisie de l'utilisateur
    """
    emoji = "❓" if show_emoji else ""
    return input(colored(f"{emoji} {message}", "magenta"))
